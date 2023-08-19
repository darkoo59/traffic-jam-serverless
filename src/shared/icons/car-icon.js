import L from 'leaflet';
import trafficJamMarker from '../../images/traffic-jam.svg';
import ambulanceMaker from '../../images/ambulance.svg';
import policeMaker from '../../images/police.svg';
import carCrashMaker from '../../images/car-crash.svg';
import firefightersMaker from '../../images/firefighters.svg';

const iconTrafficJam = new L.Icon({
    iconUrl: trafficJamMarker,
    iconRetinaUrl: trafficJamMarker,
    popupAnchor:  [-0, -0],
    iconSize: [25,40],     
});

const iconAmbulance = new L.Icon({
    iconUrl: ambulanceMaker,
    iconRetinaUrl: ambulanceMaker,
    popupAnchor:  [-0, -0],
    iconSize: [25,40],     
});

const iconPolice = new L.Icon({
    iconUrl: policeMaker,
    iconRetinaUrl: policeMaker,
    popupAnchor:  [-0, -0],
    iconSize: [25,40],     
});

const iconCarCrash = new L.Icon({
    iconUrl: carCrashMaker,
    iconRetinaUrl: carCrashMaker,
    popupAnchor:  [-0, -0],
    iconSize: [25,40],     
});

const iconFirefighters = new L.Icon({
    iconUrl: firefightersMaker,
    iconRetinaUrl: firefightersMaker,
    popupAnchor:  [-0, -0],
    iconSize: [25,40],
});

export { iconAmbulance, iconCarCrash, iconFirefighters, iconPolice, iconTrafficJam};
