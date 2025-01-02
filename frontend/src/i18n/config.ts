'use client';

import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

import zhCN from './locales/zh-CN';
import enUS from './locales/en-US';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      zh: {
        translation: zhCN,
      },
      en: {
        translation: enUS,
      },
    },
    lng: 'zh',
    fallbackLng: 'zh',
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;