import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import Container from '@mui/material/Container/Container';
import Box from '@mui/material/Box/Box';
import Avatar from '@mui/material/Avatar/Avatar';
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import { iconAmbulance, iconCarCrash, iconFirefighters, iconPolice, iconTrafficJam } from '../../icons/car-icon';

const Map = () => {


  return (
    <Container component="main" maxWidth="xs">
    <Box
      sx={{
        marginTop: 8,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
    <MapContainer style={{ height: "450px", width: "100%" }} center={[51.505, -0.09]} zoom={13} scrollWheelZoom={false} >
        <TileLayer
            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={[51.505, -0.09]} icon={iconPolice}>
            <Popup>
            A pretty CSS3 popup. <br /> Easily customizable.
            </Popup>
        </Marker>
    </MapContainer>
    </Box>
    </Container>
  )
}

export default Map;