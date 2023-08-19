import { useEffect, useState } from 'react';
import axios from 'axios';
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet'
import Container from '@mui/material/Container/Container';
import Box from '@mui/material/Box/Box';
import Backdrop from '@mui/material/Backdrop/Backdrop'
import CircularProgress from '@mui/material/CircularProgress/CircularProgress'
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
import { toast } from "react-toastify";
import { environment } from '../../../environments/environment';

const Map = () => {

  const [selectedIcon, setSelectedIcon] = React.useState(iconTrafficJam)
  const [selectedType, setSelectedType] = React.useState('')
  const [loading, setLoading] = React.useState(true);

  const iconMapping: Record<string, L.Icon> = {
    'Traffic jam': iconTrafficJam,
    'Car crash': iconCarCrash,
    'Ambulance': iconAmbulance,
    'Police': iconPolice,
    'Firefighters': iconFirefighters,
  };

  const fetchMarkers = () => {
    setLoading(true)
    fetch(`${environment.openfaas_url}/get-markers`)
      .then((response) => response.json())
      .then((data) => {
        if (data && data.markers_data) {
          const updatedMarkerData = data.markers_data.map((marker: any) => ({
            ...marker,
            icon: iconMapping[marker.type] || iconTrafficJam,
          }));
          setMarkerData(updatedMarkerData);
          setLoading(false)
        }
      })
      .catch((error) => {
        toast.error("Error while retrieving data:", error);
        setLoading(false)
      });
  };

  useEffect(() => {
    // Fetch marker data from the URL on page load
    fetchMarkers();
  }, []);


  const addMarkerToDatabase = (lat: number, lng: number, type: string) => {
    const requestData = {
      lat: lat,
      lng: lng,
      type: type,
    };
  

    axios.post(`${environment.openfaas_url}/add-marker`, requestData)
      .then((response) => {
        // Handle successful response, if needed
        toast.success('Marker added successfully');
        fetchMarkers()
      })
      .catch((error:any) => {
        if (error.response?.request.status === 405) {
          toast.info("Invalid request method!");
        } else if (error.response?.request.status === 400) {
          toast.error("Missing required data!");
        } else {
          toast.error(error.response?.request.message);
        }
        // Handle error, if needed
        toast.error('Error adding marker')
      });
  };

  const handleChange = (event: SelectChangeEvent) => {
    setSelectedType(event.target.value as string)
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

  interface LocationMarkersProps {
    markerData: MarkerIcon[];
  }

  function LocationMarkers( {markerData}: LocationMarkersProps ) {
  //   const initialMarker: MarkerIcon = {
  //     lat: 51.505,
  //     lng: -0.09,
  //     icon: iconTrafficJam
  // };
    const [markers, setMarkers] = React.useState<MarkerIcon[]>([]);
    useEffect(() => {
      if (markerData) {
        const updatedMarkers = markerData.map((marker) => ({
          ...marker,
          icon: iconMapping[marker.type] || iconTrafficJam, // Default to iconTrafficJam if type is not found
        }));
        setMarkers(updatedMarkers);
      }
    }, [markerData]);
  
    const map = useMapEvents({
      click(e: LeafletMouseEvent) {
        const newMarker: MarkerIcon = {
          lat: e.latlng.lat,
          lng: e.latlng.lng,
          icon: selectedIcon,
          type: selectedType
        }
        addMarkerToDatabase(e.latlng.lat, e.latlng.lng, selectedType);
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

  const [markerData, setMarkerData] = useState<MarkerIcon[]>([]);
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
        <LocationMarkers markerData={markerData}/>
    </MapContainer>
    </Box>
    <Backdrop
        sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={loading}
      >
        <CircularProgress color="inherit" />
      </Backdrop>
    </Container>
  )
}

export default Map;