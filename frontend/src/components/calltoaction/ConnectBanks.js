import React from 'react';
import { Button } from 'primereact/button';

const ConnectBanks = () => {
    return (
        <div className="w-6 border-round flex shadow-2">
                <div className="bg-blue-50 flex align-items-center justify-content-center py-3 px-5">
                    <img src="/teller.svg" alt="Image" className="bg-auto mx-auto block mb-4 w-full" />
                </div>
                <div className="py-3 px-5 flex flex-column align-items-start">
                    <div className="text-900 font-medium mb-2 text-xl">Connect Your Bank Account</div>
                    <p className="mt-0 mb-4 p-0 line-height-3">Teller Connect enables users to securely access their bank accounts by providing a robust API that adheres to the highest security standards, ensuring data encryption and safe transmission of sensitive information. By leveraging OAuth-based authentication, Teller Connect maintains user privacy and mitigates risks associated with traditional bank integrations.</p>
                    <a href="https://cardmath.ai/connect">
                        <Button  label="Proceed" className="mt-auto" />
                    </a>
                </div>
            </div>
    );
};

export default ConnectBanks;
