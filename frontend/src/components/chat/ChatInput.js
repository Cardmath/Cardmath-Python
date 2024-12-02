import React, { useState } from 'react';
import { InputTextarea } from 'primereact/inputtextarea';
import { Button } from 'primereact/button';
const ChatInput = ({ onSend, disabled }) => {
    const [message, setMessage] = useState('');
    
    const handleSend = () => {
        if (message.trim()) {
            onSend(message);
            setMessage('');
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey && !disabled) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="flex mt-3 p-2 shadow-1 w-6">
            <InputTextarea
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                className="mr-2 flex"
                rows={1}
                placeholder="Type a message..."
                autoResize
                onKeyDown={handleKeyPress}
                disabled={disabled}
            />
            <Button
                icon="pi pi-send"
                className="p-button-rounded p-button-primary"
                onClick={handleSend}
                disabled={disabled || !message.trim()}
                tooltip="Send"
                tooltipOptions={{ position: 'top' }}
            />
        </div>
    );
};

export default ChatInput;
