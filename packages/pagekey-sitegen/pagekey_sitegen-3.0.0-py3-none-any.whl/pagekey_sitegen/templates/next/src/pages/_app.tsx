import { createTheme, MantineProvider } from '@mantine/core';
import Layout from '@/lib/Layout'
import '@/styles/globals.css'
import '@mantine/core/styles.css';
import type { AppProps } from 'next/app'

const theme = createTheme({});

export default function App({ Component, pageProps }: AppProps) {
  return (
    <MantineProvider theme={theme}>
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </MantineProvider>
  )
}
