import React from 'react';
import { InputText } from 'primereact/inputtext';
import { Button } from 'primereact/button';

const NameInputForm = ({ onSubmit }) => {
  const [name, setName] = React.useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (name.trim()) {
      onSubmit(name.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <span className="p-float-label">
          <InputText
            id="firstName"
            value={name}
            onChange={(e) => setName(e.target.value)}
            autoFocus
          />
          <label htmlFor="firstName">Your first name</label>
        </span>
      </div>
      <div style={{ marginTop: '1rem' }}>
        <Button 
          type="submit"
          disabled={!name.trim()}
          label="Continue"
          style={{ width: '100%' }}
        />
      </div>
    </form>
  );
};

// Export both the component and the page configuration
const NameInputPage = {
  title: "Let's get to know you",
  content: "Please share your first name with us",
  primaryColor: 'var(--onb-cyan)',
  secondaryColor: 'var(--onb-green)',
  additionalContent: NameInputForm // Export the component directly instead of wrapping it
};

export default NameInputPage;