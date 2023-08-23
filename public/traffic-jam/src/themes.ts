import { ThemeOptions } from "@mui/material";

const mode = 'dark';
const primary = '#9148A1';
const background = '#000000';
const secondary = '#C46ED6';
const error = '#590047';
const textPrimary = '#ffffff';
const paperBackground = '#000000';

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