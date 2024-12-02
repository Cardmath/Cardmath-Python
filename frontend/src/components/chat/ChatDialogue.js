import React, { useRef, useEffect } from 'react';
import ChatMessage from './ChatMessage';

const ChatDialogue = ({ messages }) => {
    const messagesEndRef = useRef(null);

    // Scroll to bottom when messages change
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });     
    }, [messages]);

    return (
        <div className="flex">
            <div className="flex flex-column">
                {messages.map((msg, index) => (
                    <ChatMessage
                        key={index}
                        message={msg.content || (msg.isUser ? '' : '...')}
                        isUser={msg.isUser}
                    />
                ))}
                <div ref={messagesEndRef} />
            </div>
        </div>
    );
};

export default ChatDialogue;