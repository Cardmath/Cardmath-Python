from creditcard.schemas import CreditCardKeyMetadata
from creditcard.structure.rewardsccapi import get_card
from creditcard.structure.rewardsccapi import get_card
from creditcard.structure.update import generate_metadata
from creditcard.structure.update import get_target_update, update_field, BaseTargetUpdate
from database.creditcard.creditcard import CreditCard
from database.creditcard.source import CreditCardSource, CreditCardUpdateTaskQueue, UpdateableSourceColumns
from database.sql_alchemy_db import SyncSessionGenerator
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Tuple, Optional, Union
        
from tqdm import tqdm


import numpy as np
import pandas as pd

def task_queue_size(db: Session):
    return db.query(
        func.count(
            func.distinct(
                CreditCardUpdateTaskQueue.name,
                CreditCardUpdateTaskQueue.issuer,
                CreditCardUpdateTaskQueue.network,
                CreditCardUpdateTaskQueue.field,
            )
        )
    ).scalar()

def process_task_queue(db: Session):
    """
    Pops and processes a single element in the task queue
    """
    result = pop_task_queue(db)
    if not result:
        raise Exception('Nothing to pop from stack')
    source, target, field, rewardscc_dict, task = result 
    
    try:
        update: Union[BaseTargetUpdate, list[BaseTargetUpdate]] = get_target_update(field=field)

        if isinstance(update, list):
            for u in update:
                update_field(update=u, source=source, target=target, rewardscc_dict=rewardscc_dict)
        elif isinstance(update, BaseTargetUpdate):
            update_field(update=update, source=source, target=target, rewardscc_dict=rewardscc_dict)
        else:
            raise ValueError('No valid updateable object found!')
        
        db.delete(task)
        
    except Exception as e:
        db.delete(task)

    
def pop_task_queue(db: Session) -> Optional[Tuple[CreditCardSource, CreditCard, UpdateableSourceColumns, Optional[dict], CreditCardUpdateTaskQueue]]:
    """
    Pop the next task from the queue and fetch the source and target object.
    """
    # First get the task
    task = (
        db.query(CreditCardUpdateTaskQueue)
        .order_by(CreditCardUpdateTaskQueue.priority)
        .first()
    )

    if not task:
        return None

    # Then get the related objects
    result = (
        db.query(
            CreditCard,
            CreditCardSource,
        )
        .join(
            CreditCardSource,
            (CreditCardSource.name == CreditCard.name)
            & (CreditCardSource.issuer == CreditCard.issuer)
            & (CreditCardSource.network == CreditCard.network)
        )
        .filter(
            CreditCard.name == task.name,
            CreditCard.issuer == task.issuer,
            CreditCard.network == task.network
        )
        .first()
    )

    if not result:
        # If we have a task but no matching objects, clean up
        db.delete(task)
        db.commit()
        return None

    target, source = result

    # Fetch additional data if the source key exists
    rewardscc_dict = None
    if source.key:
        rewardscc_dict = get_card(cardKey=source.key)
    
    return source, target, task.field, rewardscc_dict, task

def clean_value(value):
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return None
    return value

def insert_from_csv(path: str, override_metadata: bool = False):
    df = pd.read_csv(path)
    pbar = tqdm(df.iterrows(), total=len(df), desc="Processing CSV rows")
    skipped = 0
    
    for index, row in pbar:
        metadata: CreditCardKeyMetadata = generate_metadata(row['dump'])
        metadata.key = None
        if override_metadata:
            overrides = {key: value for key, value in row.iloc[:4].to_dict().items() if value}
            metadata = metadata.model_copy(update=overrides)
        
        metadata_dict = {key: clean_value(value) for key, value in metadata.model_dump().items()}
        remainder_dict = {key: clean_value(value) for key, value in row.iloc[4:].to_dict().items()}

        try:    
            with SyncSessionGenerator.begin() as db:
                db.add(
                    CreditCardSource(
                        **metadata_dict,
                        **remainder_dict
                    )
                )
                db.commit()
        except IntegrityError:
            skipped += 1
            pbar.set_postfix({'Could not insert': {metadata.model_dump_json()}}, refresh=True)
        except KeyboardInterrupt:
            pbar.write("\nTerminated Insertion From CSV")
            break

def empty_task_queue():
    size = 0
    with SyncSessionGenerator.begin() as db:
        size = task_queue_size(db=db)
    
    # Create progress bar
    with tqdm(total=size, desc="Processing tasks") as pbar:
        for i in range(size):
            try: 
                with SyncSessionGenerator.begin() as db:
                    process_task_queue(db=db)
                pbar.update(1)  # Update progress bar after each successful task
            except KeyboardInterrupt:
                print("\nStopped Emptying the task queue before it was empty. You can rerun this method to continue emptying the queue.")
                break