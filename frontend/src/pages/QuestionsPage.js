import React, { useState } from 'react';
import { InputText } from 'primereact/inputtext';
import { Button } from 'primereact/button';
import { Dropdown } from 'primereact/dropdown';
import { Calendar } from 'primereact/calendar';

const QuestionsPage = () => {
    const [formData, setFormData] = useState({
        favoriteBank: '',
        favoriteAirline: '',
        birthDate: null,
        favoriteColor: ''
    });

    const banks = [
        { label: 'Bank of America', value: 'Bank of America' },
        { label: 'Chase', value: 'Chase' },
        { label: 'Wells Fargo', value: 'Wells Fargo' }
    ];

    const airlines = [
        { label: 'American Airlines', value: 'American Airlines' },
        { label: 'Delta', value: 'Delta' },
        { label: 'United Airlines', value: 'United Airlines' }
    ];

    const colors = [
        { label: 'Red', value: 'Red' },
        { label: 'Blue', value: 'Blue' },
        { label: 'Green', value: 'Green' }
    ];

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(formData);
    };

    return (
        <div className="p-grid p-justify-center">
            <div className="p-col-12 p-md-6">
                <h2>Questions Form</h2>
                <form onSubmit={handleSubmit}>
                    <div className="p-field">
                        <label htmlFor="favoriteBank">What is your favorite bank?</label>
                        <Dropdown id="favoriteBank" name="favoriteBank" value={formData.favoriteBank} options={banks} onChange={handleChange} placeholder="Select a Bank" />
                    </div>
                    <div className="p-field">
                        <label htmlFor="favoriteAirline">What is your favorite airline?</label>
                        <Dropdown id="favoriteAirline" name="favoriteAirline" value={formData.favoriteAirline} options={airlines} onChange={handleChange} placeholder="Select an Airline" />
                    </div>
                    <div className="p-field">
                        <label htmlFor="birthDate">What is your birth date?</label>
                        <Calendar id="birthDate" name="birthDate" value={formData.birthDate} onChange={handleChange} showIcon />
                    </div>
                    <div className="p-field">
                        <label htmlFor="favoriteColor">What is your favorite color?</label>
                        <Dropdown id="favoriteColor" name="favoriteColor" value={formData.favoriteColor} options={colors} onChange={handleChange} placeholder="Select a Color" />
                    </div>
                    <Button type="submit" label="Submit" />
                </form>
            </div>
        </div>
    );
};

export default QuestionsPage;