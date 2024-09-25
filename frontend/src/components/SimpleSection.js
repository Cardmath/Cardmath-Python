import React from 'react';

const SimpleSection = ( {sectionTitle} ) => {
    return (
        <div className="surface-ground px-4 py-5 md:px-6 lg:px-8">
            <div className="border-bottom-1 surface-border">
                <span className="block text-3xl font-medium text-900 mb-4">{sectionTitle}</span>
            </div>
        </div>
    );
};

export default SimpleSection;