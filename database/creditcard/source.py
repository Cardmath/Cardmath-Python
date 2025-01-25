from database.sql_alchemy_db import Base
from enum import StrEnum
from sqlalchemy import Column, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import TEXT, ENUM, DATE, ARRAY, INTEGER

class CreditCardSource(Base):
    __tablename__ = "credit_cards_source"

    name = Column(TEXT,  nullable=False, primary_key=True)
    issuer = Column(TEXT, nullable=False, primary_key=True)
    network = Column(TEXT, nullable=False, primary_key=True)
    key = Column(TEXT, unique=True, nullable=True)

    reference_links = Column(ARRAY(TEXT), nullable=True)
    source_last_verified = Column(DATE, nullable=True)    
    
    dump = Column(TEXT, nullable=False)

    reward_category_map = Column(TEXT, nullable=True)      

    sign_on_bonus = Column(TEXT, nullable=True)
    annual_fee = Column(TEXT, nullable=True)
    statement_credit = Column(TEXT, nullable=True)

    benefits = Column(TEXT, nullable=True)
    apr = Column(TEXT, nullable=True)
    credit_needed = Column(TEXT, nullable=True) 
    keywords = Column(TEXT, nullable=True)

class UpdateableSourceColumns(StrEnum):
    DUMP = 'dump'
    REWARD_CATEGORY_MAP = 'reward_category_map'
    SIGN_ON_BONUS = 'sign_on_bonus'
    ANNUAL_FEE = 'annual_fee'
    STATEMENT_CREDIT = 'statement_credit'
    BENEFITS = 'benefits'
    APR = 'apr'
    CREDIT_NEEDED = 'credit_needed'
    KEYWORDS = 'keywords'

credit_card_attribute_enum = ENUM(
    UpdateableSourceColumns,
    name='cc_attr_enum',
    metadata=Base.metadata,
    values_callable=lambda enum: [e.value for e in enum],
    create_type=True,
)

class CreditCardUpdateTaskQueue(Base):
    __tablename__ = "credit_cards_update"

    name = Column(TEXT, primary_key=True)
    issuer = Column(TEXT, primary_key=True)
    network = Column(TEXT, primary_key=True)

    priority = Column(INTEGER, index=True, autoincrement=True)
    field = Column(credit_card_attribute_enum, primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ['name', 'issuer', 'network'],
            ['credit_cards_source.name', 'credit_cards_source.issuer', 'credit_cards_source.network'],
        ),
    )

insert_update_sql = """
CREATE OR REPLACE FUNCTION notify_credit_card_update()
RETURNS TRIGGER AS $$
BEGIN
-- For INSERT operations, OLD is null, so we want to add all non-null fields
    IF TG_OP = 'INSERT' THEN
        -- Always add dump for new rows since it's required
        INSERT INTO credit_cards_update (name, issuer, network, field)
        VALUES (NEW.name, NEW.issuer, NEW.network, 'dump');

        IF NEW.reward_category_map IS NOT NULL THEN
            INSERT INTO credit_cards_update (name, issuer, network, field)
            VALUES (NEW.name, NEW.issuer, NEW.network, 'reward_category_map');
        END IF;

        IF NEW.sign_on_bonus IS NOT NULL THEN
            INSERT INTO credit_cards_update (name, issuer, network, field)
            VALUES (NEW.name, NEW.issuer, NEW.network, 'sign_on_bonus');
        END IF;

        IF NEW.annual_fee IS NOT NULL THEN
            INSERT INTO credit_cards_update (name, issuer, network, field)
            VALUES (NEW.name, NEW.issuer, NEW.network, 'annual_fee');
        END IF;

        IF NEW.statement_credit IS NOT NULL THEN
            INSERT INTO credit_cards_update (name, issuer, network, field)
            VALUES (NEW.name, NEW.issuer, NEW.network, 'statement_credit');
        END IF;

        IF NEW.benefits IS NOT NULL THEN
            INSERT INTO credit_cards_update (name, issuer, network, field)
            VALUES (NEW.name, NEW.issuer, NEW.network, 'benefits');
        END IF;

        IF NEW.apr IS NOT NULL THEN
            INSERT INTO credit_cards_update (name, issuer, network, field)
            VALUES (NEW.name, NEW.issuer, NEW.network, 'apr');
        END IF;

        IF NEW.credit_needed IS NOT NULL THEN
            INSERT INTO credit_cards_update (name, issuer, network, field)
            VALUES (NEW.name, NEW.issuer, NEW.network, 'credit_needed');
        END IF;

        IF NEW.keywords IS NOT NULL THEN
            INSERT INTO credit_cards_update (name, issuer, network, field)
            VALUES (NEW.name, NEW.issuer, NEW.network, 'keywords');
        END IF;
    ELSE
        -- For UPDATE operations, check dump changes first
        IF NEW.dump IS DISTINCT FROM OLD.dump THEN
            INSERT INTO credit_cards_update (name, issuer, network, field)
            VALUES (NEW.name, NEW.issuer, NEW.network, 'dump');
        END IF;

        -- Check reward_category_map changes
        IF NEW.reward_category_map IS DISTINCT FROM OLD.reward_category_map THEN
            INSERT INTO credit_cards_update (name, issuer, network, field)
            VALUES (NEW.name, NEW.issuer, NEW.network, 'reward_category_map');
        END IF;

        -- Check sign_on_bonus changes
        IF NEW.sign_on_bonus IS DISTINCT FROM OLD.sign_on_bonus THEN
            INSERT INTO credit_cards_update (name, issuer, network, field)
            VALUES (NEW.name, NEW.issuer, NEW.network, 'sign_on_bonus');
        END IF;

        -- Check annual_fee changes
        IF NEW.annual_fee IS DISTINCT FROM OLD.annual_fee THEN
            INSERT INTO credit_cards_update (name, issuer, network, field)
            VALUES (NEW.name, NEW.issuer, NEW.network, 'annual_fee');
        END IF;

        -- Check statement_credit changes
        IF NEW.statement_credit IS DISTINCT FROM OLD.statement_credit THEN
            INSERT INTO credit_cards_update (name, issuer, network, field)
            VALUES (NEW.name, NEW.issuer, NEW.network, 'statement_credit');
        END IF;

        -- Check benefits changes
        IF NEW.benefits IS DISTINCT FROM OLD.benefits THEN
            INSERT INTO credit_cards_update (name, issuer, network, field)
            VALUES (NEW.name, NEW.issuer, NEW.network, 'benefits');
        END IF;

        -- Check apr changes
        IF NEW.apr IS DISTINCT FROM OLD.apr THEN
            INSERT INTO credit_cards_update (name, issuer, network, field)
            VALUES (NEW.name, NEW.issuer, NEW.network, 'apr');
        END IF;

        -- Check credit_needed changes
        IF NEW.credit_needed IS DISTINCT FROM OLD.credit_needed THEN
            INSERT INTO credit_cards_update (name, issuer, network, field)
            VALUES (NEW.name, NEW.issuer, NEW.network, 'credit_needed');
        END IF;

        -- Check keywords changes
        IF NEW.keywords IS DISTINCT FROM OLD.keywords THEN
            INSERT INTO credit_cards_update (name, issuer, network, field)
            VALUES (NEW.name, NEW.issuer, NEW.network, 'keywords');
        END IF;

        -- Note: We don't track changes to 'key' field as it's not part of the enum
        -- and doesn't need synchronization
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

register_update_insert_trigger = """
CREATE TRIGGER credit_card_update_trigger
    AFTER INSERT OR UPDATE ON credit_cards_source
    FOR EACH ROW
    EXECUTE FUNCTION notify_credit_card_update();
"""

create_credit_card_sql = """
CREATE OR REPLACE FUNCTION create_credit_card()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO credit_cards (
        name,
        issuer,
        network,
        key,
        referral_link,
        last_verified,
        user_feedback,
        reward_category_map,
        primary_reward_unit,
        sign_on_bonus,
        annual_fee,
        statement_credit,
        benefits,
        apr,
        credit_needed,
        keywords
    ) VALUES (
        NEW.name,
        NEW.issuer,
        NEW.network,
        NEW.key,
        NULL,
        NULL,
        ARRAY[]::TEXT[], -- default empty array for user_feedback
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

register_create_credit_card_trigger = """
CREATE TRIGGER credit_card_source_after_insert
    AFTER INSERT ON credit_cards_source
    FOR EACH ROW
    EXECUTE FUNCTION create_credit_card();
"""