import { ThemeOptions } from "@mui/material";

const mode = 'light';
const primary = '#b9b9b9';
const background = '#f0f0f0 ';
const secondary = '#b9b9b9';
const error = '#590047';
const textPrimary = '#ffffff';
const paperBackground = '#b9b9b9';

const defaultThemeOptions: ThemeOptions = {
  palette: {
    mode: mode,
    primary: {
      main: primary,
    },
    background: {
      default: background,
      paper: background,
    },
    secondary: {
      main: secondary,
    },
    error: {
      main: error,
    },
  },
  components: {
    MuiTypography: {
      defaultProps: {
        color: '#9148A1'
      }
    },
    MuiPaper: {
      defaultProps: {
        sx: {
          backgroundColor: paperBackground
        }
      }
    }
  }
};

export { defaultThemeOptions }