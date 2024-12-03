import React, { useState, useEffect, useRef } from 'react';
import ChatInput from './ChatInput';
import ChatCallToAction from './ChatCallToAction';
import ChatDialogue from './ChatDialogue';
import { fetchWithAuth } from '../../pages/AuthPage';
import { getBackendUrl } from '../../utils/urlResolver';

const ChatContainer = () => {
    const [messages, setMessages] = useState([]);
    const [isStreaming, setIsStreaming] = useState(false);
    const bufferRef = useRef('');
    
    const handleSend = async (content) => {
        const userMessage = {
            content,
            isUser: true,
            timestamp: new Date()
        };
        
        setMessages(prev => [...prev, userMessage]);
        
        const assistantMessage = {
            content: "",
            isUser: false,
            timestamp: new Date(),
            id: Date.now()
        };
        
        setMessages(prev => [...prev, assistantMessage]);
        setIsStreaming(true);

        let reader;
        try {
            const response = await fetchWithAuth(`${getBackendUrl()}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'text/event-stream',
                },
                body: JSON.stringify({ message: content })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { value, done } = await reader.read();
                
                if (done) break;
                
                // Decode the chunk and add it to our buffer
                const chunk = decoder.decode(value, { stream: true });
                bufferRef.current += chunk;
                
                
                const tokens = bufferRef.current.split(' ');
                bufferRef.current = tokens.pop() || '';

                for (const token of tokens) {
                    if (!token) continue;                    
                    if (token === '[DONE]') {
                        setIsStreaming(false);
                        return;
                    }

                    await new Promise(resolve => setTimeout(resolve, 20));

                    setMessages(prev => {
                        const newMessages = [...prev];
                        const lastMessage = newMessages[newMessages.length - 1];
                        lastMessage.content = (lastMessage.content || '') + token;
                        lastMessage.id = Date.now(); // Force re-render
                        return newMessages;
                    });
                }
            }
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => {
                const updated = [...prev];
                updated[updated.length - 1].content = "Sorry, there was an error generating the response: " + error.message;
                return updated;
            });
        } finally {
            setIsStreaming(false);
            bufferRef.current = '';
            if (reader) {
                reader.releaseLock();
            }
        }
    };

    return (
        <div className="flex flex-column align-items-center justify-content-center w-full h-screen bg-gray-800">
            <ChatCallToAction />
            <ChatDialogue messages={messages} />
            <ChatInput 
                onSend={handleSend} 
                disabled={isStreaming}
            />
            {isStreaming && (
                <div className="text-white mt-2">
                    Processing...
                </div>
            )}
        </div>
    );
};

export default ChatContainer;