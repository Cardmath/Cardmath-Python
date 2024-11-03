import React, { useState, useEffect } from 'react';
import { Card } from 'primereact/card';
import { Carousel } from 'primereact/carousel';
import { Dialog } from 'primereact/dialog';
import { PickList } from 'primereact/picklist';
import { Button } from 'primereact/button';
import { Tooltip } from 'primereact/tooltip';
import { ConfirmDialog, confirmDialog } from 'primereact/confirmdialog';
import { InputText } from 'primereact/inputtext'; // Import InputText component
import { fetchWithAuth } from '../pages/AuthPage';
import moment from 'moment';

const WalletDisplay = ({ wallets, loading, error, onWalletUpdate }) => {
  const [showDialog, setShowDialog] = useState(false);
  const [availableCards, setAvailableCards] = useState([]);
  const [newWalletCards, setNewWalletCards] = useState([]);
  const [walletName, setWalletName] = useState("");
  const [editingWallet, setEditingWallet] = useState(null);
  const [isNameInvalid, setIsNameInvalid] = useState(false);

  useEffect(() => {
    fetch("http://localhost:8000/read_credit_cards_database", {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ card_details: "all", use_preferences: false })
    })
    .then(response => response.json())
    .then(data => {
      setAvailableCards(data.credit_card || []);
    })
    .catch(error => console.error("Error fetching cards:", error));
  }, []);

  const openDialog = (wallet = null) => {
    if (wallet) {
      setWalletName(wallet.name);
      setNewWalletCards(wallet.cards.map(card => ({
        name: card.card.name,
        issuer: card.card.issuer
      })));
      setEditingWallet(wallet);
    } else {
      setWalletName("");
      setNewWalletCards([]);
      setEditingWallet(null);
    }
    setShowDialog(true);
  };

  const closeDialog = () => {
    setShowDialog(false);
    setWalletName("");
    setNewWalletCards([]);
    setIsNameInvalid(false); // Reset name validity
  };

  const saveWallet = async () => {
    if (!walletName.trim()) {
      setIsNameInvalid(true); // Set invalid if wallet name is empty
      return;
    }

    const walletData = {
      wallet_id: editingWallet ? editingWallet.id : undefined,
      name: walletName,
      is_custom: true,
      cards: newWalletCards.map(card => ({
        name: card.name,
        issuer: card.issuer
      }))
    };

    try {
      const endpoint = editingWallet
        ? "http://localhost:8000/edit_user_wallet"
        : "http://localhost:8000/ingest_user_wallet";
      
      const response = await fetchWithAuth(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(walletData)
      });

      if (response.ok) {
        closeDialog();
        onWalletUpdate(); // Refresh wallets after adding or editing
      } else {
        console.error("Failed to save wallet:", await response.text());
      }
    } catch (error) {
      console.error("Error saving wallet:", error);
    }
  };

  const confirmDeleteWallet = (walletId) => {
    confirmDialog({
      message: "Are you sure you want to delete this wallet?",
      header: "Confirm Delete",
      icon: "pi pi-exclamation-triangle",
      accept: () => deleteWallet(walletId),
    });
  };

  const deleteWallet = async (walletId) => {
    try {
      const response = await fetchWithAuth("http://localhost:8000/delete_user_wallet", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ wallet_id: walletId })
      });

      if (response.ok) {
        onWalletUpdate(); // Refresh wallets after deletion
      } else {
        console.error("Failed to delete wallet:", await response.text());
      }
    } catch (error) {
      console.error("Error deleting wallet:", error);
    }
  };

  const onChangePickList = (event) => {
    setNewWalletCards(event.target);
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

  if (loading) {
    return <p>Loading wallets...</p>;
  }

  if (error) {
    return <p className="text-red-500">{error}</p>;
  }

  return (
    <div className="flex flex-wrap gap-4 justify-content-start p-4">
      <ConfirmDialog /> {/* ConfirmDialog component at the top level */}

      <Card 
        className="flex flex-column align-items-center justify-content-center p-5 w-3 shadow-3 cursor-pointer surface-200 border-round" 
        onClick={() => openDialog()}
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
              <Button label="Edit" icon="pi pi-pencil" onClick={() => openDialog(wallet)} className="mt-2 mr-4" />
              <Button 
                label="Delete" 
                icon="pi pi-trash" 
                onClick={() => confirmDeleteWallet(wallet.id)} 
                className="mt-2 p-button-danger" 
              />
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
        header={editingWallet ? "Edit Wallet" : "Create New Wallet"} 
        visible={showDialog} 
        style={{ width: '50vw' }} 
        modal 
        onHide={closeDialog}  
        footer={
          <div>
            <Button 
              label="Save" 
              icon="pi pi-check" 
              onClick={saveWallet} 
              autoFocus 
              disabled={!walletName.trim()}
            />
            <Button label="Cancel" icon="pi pi-times" onClick={closeDialog} className="p-button-text" />
          </div>
        }
      >
        <span className="p-float-label mb-3">
          <InputText
            id="walletName"
            value={walletName}
            onChange={(e) => {
              setWalletName(e.target.value);
              setIsNameInvalid(!e.target.value.trim());
            }}
            className={isNameInvalid ? ' p-invalid ' : ''}
            tooltip="Wallet name is required"
            tooltipOptions={{ position: 'right', event: 'focus' }}
            placeholder="Wallet Name"
          />
        </span>
        
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
