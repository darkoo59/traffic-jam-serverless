import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet'
import Container from '@mui/material/Container/Container';
import Box from '@mui/material/Box/Box';
import Avatar from '@mui/material/Avatar/Avatar';
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import { iconAmbulance, iconCarCrash, iconFirefighters, iconPolice, iconTrafficJam } from '../../icons/car-icon';
import FormControl from '@mui/material/FormControl/FormControl';
import InputLabel from '@mui/material/InputLabel/InputLabel';
import Select, { SelectChangeEvent } from '@mui/material/Select/Select';
import MenuItem from '@mui/material/MenuItem/MenuItem';
import React from 'react';
import { DivIcon, Icon, IconOptions, LatLng, LeafletMouseEvent} from 'leaflet';
import {MarkerIcon} from '../../models/marker'

const Map = () => {

  const [selectedIcon, setSelectedIcon] = React.useState(iconTrafficJam)

  const handleChange = (event: SelectChangeEvent) => {
    if(event.target.value as string == 'Traffic jam')
      setSelectedIcon(iconTrafficJam)
    else if(event.target.value as string == 'Car crash')
      setSelectedIcon(iconCarCrash)
    else if(event.target.value as string == 'Ambulance')
      setSelectedIcon(iconAmbulance)
    else if(event.target.value as string == 'Police')
      setSelectedIcon(iconPolice)
    else if(event.target.value as string == 'Firefighters')
      setSelectedIcon(iconFirefighters)
  };

  function LocationMarkers() {
    const initialMarker: MarkerIcon = {
      lat: 51.505,
      lng: -0.09,
      icon: iconTrafficJam
  };
    const [markers, setMarkers] = React.useState<MarkerIcon[]>([initialMarker]);
  
    const map = useMapEvents({
      click(e: LeafletMouseEvent) {
        const newMarker: MarkerIcon = {
          lat: e.latlng.lat,
          lng: e.latlng.lng,
          icon: selectedIcon
        }
        const newMarkers = [...markers,newMarker];
        setMarkers(newMarkers);
      },
    });
  
    return (
      <React.Fragment>
        {markers.map((markerr, index) => (
          <Marker key={index} position={new LatLng(markerr.lat, markerr.lng)} icon={markerr.icon}></Marker>
        ))}
      </React.Fragment>
    );
  }


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

  <FormControl fullWidth>
    <InputLabel id="demo-simple-select-label">Marker type</InputLabel>
    <Select
      labelId="demo-simple-select-label"
      id="demo-simple-select"
      label="Marker type"
      onChange={handleChange}
      defaultValue={'Traffic jam'}
    >
      <MenuItem value={'Traffic jam'}>Traffic jam</MenuItem>
      <MenuItem value={'Car crash'}>Car crash</MenuItem>
      <MenuItem value={'Ambulance'}>Ambulance</MenuItem>
      <MenuItem value={'Police'}>Police</MenuItem>
      <MenuItem value={'Firefighters'}>Firefighters</MenuItem>
    </Select>
  </FormControl>

    <MapContainer style={{ height: "450px", width: "100%" }} center={[51.505, -0.09]} zoom={13} scrollWheelZoom={false} >
        <TileLayer
            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {/* <Marker position={[51.505, -0.09]} icon={iconPolice}>
            <Popup>
            A pretty CSS3 popup. <br /> Easily customizable.
            </Popup>
        </Marker> */}
        <LocationMarkers/>
    </MapContainer>
    </Box>
    </Container>
  )
}

export default Map;