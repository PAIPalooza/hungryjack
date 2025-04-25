import { extendTheme, type ThemeConfig } from '@chakra-ui/react';
import { Dict } from '@chakra-ui/utils';

// Color palette
const colors = {
  brand: {
    50: '#e8f5e9',
    100: '#c8e6c9',
    200: '#a5d6a7',
    300: '#81c784',
    400: '#66bb6a',
    500: '#4caf50', // Primary green
    600: '#43a047',
    700: '#388e3c',
    800: '#2e7d32',
    900: '#1b5e20',
  },
  accent: {
    50: '#fff8e1',
    100: '#ffecb3',
    200: '#ffe082',
    300: '#ffd54f',
    400: '#ffca28',
    500: '#ffc107', // Accent yellow
    600: '#ffb300',
    700: '#ffa000',
    800: '#ff8f00',
    900: '#ff6f00',
  }
};

// Font configuration
const fonts = {
  heading: '"Poppins", sans-serif',
  body: '"Open Sans", sans-serif',
};

// Component style overrides
const components = {
  Button: {
    baseStyle: {
      fontWeight: 'semibold',
      borderRadius: 'md',
    },
    variants: {
      solid: (props: Dict) => ({
        bg: props.colorScheme === 'green' ? 'brand.500' : undefined,
        _hover: {
          bg: props.colorScheme === 'green' ? 'brand.600' : undefined,
        },
      }),
      outline: (props: Dict) => ({
        borderColor: props.colorScheme === 'green' ? 'brand.500' : undefined,
        color: props.colorScheme === 'green' ? 'brand.500' : undefined,
        _hover: {
          bg: props.colorScheme === 'green' ? 'brand.50' : undefined,
        },
      }),
    },
    defaultProps: {
      colorScheme: 'green',
    },
  },
  Heading: {
    baseStyle: {
      fontWeight: 'semibold',
      lineHeight: 'shorter',
    },
  },
  FormLabel: {
    baseStyle: {
      fontSize: 'md',
      fontWeight: 'medium',
      mb: 2,
    },
  },
  Input: {
    variants: {
      outline: {
        field: {
          borderRadius: 'md',
          _focus: {
            borderColor: 'brand.500',
            boxShadow: '0 0 0 1px var(--chakra-colors-brand-500)',
          },
        },
      },
    },
  },
  Select: {
    variants: {
      outline: {
        field: {
          borderRadius: 'md',
          _focus: {
            borderColor: 'brand.500',
            boxShadow: '0 0 0 1px var(--chakra-colors-brand-500)',
          },
        },
      },
    },
  },
  Checkbox: {
    baseStyle: {
      control: {
        _checked: {
          bg: 'brand.500',
          borderColor: 'brand.500',
        },
      },
    },
  },
};

// Theme configuration
const config: ThemeConfig = {
  initialColorMode: 'light',
  useSystemColorMode: false,
};

// Create and export the theme
const theme = extendTheme({
  colors,
  fonts,
  components,
  config,
});

export default theme;
