import React, { createContext, useState, useContext } from 'react';
import { languages } from '../config/languages';

const LanguageContext = createContext();

export const LanguageProvider = ({ children }) => {
  const [currentLanguage, setCurrentLanguage] = useState('en');

  const changeLanguage = (langCode) => {
    if (languages[langCode]) {
      setCurrentLanguage(langCode);
    }
  };

  const t = (key) => {
    const keys = key.split('.');
    let translation = languages[currentLanguage].translations;
    
    for (const k of keys) {
      translation = translation[k];
      if (!translation) return key;
    }
    
    return translation;
  };

  return (
    <LanguageContext.Provider value={{ currentLanguage, changeLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}; 