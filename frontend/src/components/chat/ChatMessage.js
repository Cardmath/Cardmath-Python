import React, { useEffect, useState } from "react";

const ChatMessage = ({ message, isUser }) => {
    console.log("ChatMessage rendering with:", { message, isUser }); // Add logging
    const [key, setKey] = useState(Date.now());
    useEffect(() => {
        setKey(Date.now());
    }, [message]);

    return (
        <div key={key} className={`flex w-full p-3 ${isUser ? 'justify-content-end' : 'justify-content-start'}`}>
            <div className={`flex align-items-start gap-2 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
                <div className={`flex justify-content-center align-items-center border-circle p-2 ${
                    isUser ? 'bg-primary' : 'bg-gray-500'
                }`}>
                    <i className={`pi ${isUser ? 'pi-user' : 'pi-android'} text-white`}></i>
                </div>
                <div className={`flex flex-column ${isUser ? 'align-items-end' : 'align-items-start'}`}>
                    <div className={`text-sm text-gray-600 mb-1`}>
                        {isUser ? 'You' : 'Cardmath AI'}
                    </div>
                    <div className={`p-3 border-round-lg ${
                        isUser ? 'bg-primary text-white' : 'bg-gray-100 text-gray-900'
                    }`}>
                        {message}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChatMessage;