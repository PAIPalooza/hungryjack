import React from 'react';
import { AppProps } from 'next/app';
import { ChakraProvider } from '@chakra-ui/react';
import theme from '../theme';
import Head from 'next/head';
import '../styles/globals.css';

/**
 * Custom App component for HungryJack
 * Provides global theme and layout for all pages
 */
function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ChakraProvider theme={theme}>
      <Head>
        <title>HungryJack - AI Meal Planner</title>
        <meta name="description" content="AI-powered personalized meal planning based on your dietary goals and preferences" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
        <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;500;600&family=Poppins:wght@500;600;700&display=swap" rel="stylesheet" />
      </Head>
      <Component {...pageProps} />
    </ChakraProvider>
  );
}

export default MyApp;
