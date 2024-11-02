import React, { useState, useEffect } from 'react';
import { Card } from 'primereact/card';
import { Carousel } from 'primereact/carousel';
import { Dialog } from 'primereact/dialog';
import { PickList } from 'primereact/picklist';
import { Button } from 'primereact/button';
import moment from 'moment';
import { Tooltip } from 'primereact/tooltip';
import { fetchWithAuth } from '../pages/AuthPage';

const WalletDisplay = ({ wallets, loading, error, onCreateNewWallet }) => {
  const [showDialog, setShowDialog] = useState(false);
  const [availableCards, setAvailableCards] = useState([]);
  const [selectedCards, setSelectedCards] = useState([]);
  const [newWalletCards, setNewWalletCards] = useState([]);

  // Fetch all credit cards for the PickList when component mounts
  useEffect(() => {
    fetch("http://localhost:8000/read_credit_cards_database", {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ card_details: "all", use_preferences: false })
    })
    .then(response => response.json())
    .then(data => {
      setAvailableCards(data.credit_card || []); // Initialize available cards as array
    })
    .catch(error => console.error("Error fetching cards:", error));
  }, []);

  const openDialog = () => {
    setNewWalletCards(selectedCards); 
    setShowDialog(true); 
  };

  const closeDialog = () => {
    setShowDialog(false);
  };

  const saveWallet = () => {
    setSelectedCards(newWalletCards); 
    setShowDialog(false);
  };

  const sendSelectedCards = () => {
    fetchWithAuth("http://localhost:8000/create_wallet", {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ card_ids: newWalletCards.map(card => card.id) })
    })

  };

  const cardTemplate = (cardInWallet) => {
    const { card, is_held } = cardInWallet;
    return (
      <div className="flex justify-content-center">
        <Card 
          title={card.name} 
          subTitle={`Issuer: ${card.issuer}`} 
          className="w-full text-center shadow-1 p-3 border-round"
        >
          <div className="text-sm">Status: {is_held ? 'Held' : 'New'}</div>
        </Card>
      </div>
    );
  };

  const onChangePickList = (event) => {
    setNewWalletCards(event.target);
  };

  if (loading) {
    return <p>Loading wallets...</p>;
  }

  if (error) {
    return <p className="text-red-500">{error}</p>;
  }

  return (
    <div className="flex flex-wrap gap-4 justify-content-start p-4">
      <Card 
        className="flex flex-column align-items-center justify-content-center p-5 w-3 shadow-3 cursor-pointer surface-200 border-round" 
        onClick={openDialog}
      >
        <i className="pi pi-plus text-4xl text-blue-500 mb-2 pl-7"></i>
        <p className="text-blue-500 font-bold text-lg">Create New Wallet</p>
      </Card>

      {wallets.length === 0 ? (
        <p>No wallets found.</p>
      ) : (
        wallets.map((wallet) => (
          <Card 
            key={wallet.id} 
            className="flex flex-column w-3 h-auto shadow-3 border-round p-4 gap-2"
          >
            <div className="text-center mb-2">
              <h3 className="text-xl font-semibold">{wallet.name}</h3>
              <p className="text-sm text-500">
                {wallet.is_custom ? 'Custom Wallet' : 'Inferred Wallet'} <br />
                Last Edited: {moment(wallet.last_edited).format('MMMM Do, YYYY')}
              </p>
              <Tooltip target=".wallet-info" position="top" />
              <div 
                className="wallet-info text-primary text-center mt-1" 
                data-pr-tooltip="Information about this wallet's customization status and last edited date."
              >
                <i className="pi pi-info-circle text-lg"></i>
              </div>
            </div>

            {wallet.cards.length > 0 ? (
              <Carousel
                autoplayInterval={3000}
                value={wallet.cards}
                itemTemplate={cardTemplate}
                numVisible={1}
                numScroll={1}
                circular
                showNavigators
                className="w-full mt-2"
              />
            ) : (
              <div className="flex align-items-center justify-content-center p-3 text-center surface-300 border-round h-6rem">
                <p className="m-0 text-500">No credit cards available in this wallet.</p>
              </div>
            )}
          </Card>
        ))
      )}

      <Dialog 
        header="Select Cards for Wallet" 
        visible={showDialog} 
        style={{ width: '50vw' }} 
        modal 
        onHide={closeDialog}  
        footer={
          <div>
            <Button label="Save" icon="pi pi-check" onClick={saveWallet} autoFocus />
            <Button label="Cancel" icon="pi pi-times" onClick={closeDialog} className="p-button-text" />
          </div>
        }
      >
        <PickList
          source={availableCards || []}
          target={newWalletCards || []}
          onChange={onChangePickList}
          itemTemplate={(card) => (
            <div>
              <p>{card.name}</p>
              <small>{card.issuer}</small>
            </div>
          )}
          sourceHeader="Available Cards"
          targetHeader="Selected Cards"
          showSourceControls
          showTargetControls
        />
      </Dialog>
    </div>
  );
};

export default WalletDisplay;
