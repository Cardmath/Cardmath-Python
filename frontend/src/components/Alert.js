import React from 'react';

const Alert = ({ visible, heading, message, type, setVisible }) => {  
    let baseBorder = "flex align-items-start p-4 border-round border-1 ";

    const bg_color = (type) => {
        console.log('Alert invoked');
        switch(type) {
            case 'success':
                return 'bg-green-100 border-green-300';
            case 'error':
                return 'bg-pink-100 border-pink-300';
            case 'warning':
                return 'bg-yellow-50 border-yellow-100';
            case 'info':
                return 'bg-blue-50 border-blue-100';
            default:
                return '';
        }
    };

    const icon_color = (type) => {
        switch(type) {
            case 'success':
                return 'pi pi-check-circle text-green-900';
            case 'error':
                return 'pi pi-times-circle text-pink-900';
            case 'warning':
                return 'pi pi-exclamation-triangle text-yellow-900';
            case 'info':
                return 'pi pi-info-circle text-blue-900';
            default:
                return '';
        }
    };

    const text_color = (type) => {
        switch(type) {
            case 'success':
                return 'text-green-900';
            case 'error':
                return 'text-pink-900';
            case 'warning':
                return 'text-yellow-900';
            case 'info':
                return 'text-blue-900';
            default:
                return '';
        }
    };

    const button_hover_color = (type) => {
        switch(type) {
            case 'success':
                return 'hover:bg-green-50';
            case 'error':
                return 'hover:bg-pink-50';
            case 'warning':
                return 'hover:bg-yellow-50';
            case 'info':
                return 'hover:bg-blue-50';
            default:
                return '';
        }
    };

    return (
        <div>
            {visible && <div className={baseBorder + bg_color(type)} >
                <i className={icon_color(type) + " text-2xl mr-3"}></i>
                <div className="mr-3">
                    <div className={text_color(type) + " font-medium text-xl mb-2 line-height-1"}>{heading}</div>
                    <p className={"m-0 p-0 " + text_color(type) + " line-height-3"}>{message}</p>
                </div>
                <div className="ml-auto" onClick={() => setVisible(false)}>
                    <a className={"inline-flex align-items-center justify-content-center ml-auto border-circle " + button_hover_color(type) + " no-underline cursor-pointer transition-colors transition-duration-150"} style={{ width: '1.5rem', height: '1.5rem' }}>
                        <i className={text_color(type) + " pi pi-times"}></i>
                    </a>
                </div>
            </div>}
        </div>
    );
};

export default Alert;