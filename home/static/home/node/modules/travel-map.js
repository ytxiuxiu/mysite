import React from 'react';
import http from './http';

import withScriptjs from "react-google-maps/lib/async/withScriptjs";
import SearchBox from "react-google-maps/lib/places/SearchBox";
import { withGoogleMap, GoogleMap, Marker, DirectionsRenderer } from 'react-google-maps';

const TravelGoogleMap = withScriptjs(
  withGoogleMap(props => (
    <GoogleMap
      ref={props.onMapMounted}
      zoom={12}
      center={props.center}
      onBoundsChanged={props.onBoundsChanged}>

      <SearchBox
        ref={props.onSearchBoxMounted}
        bounds={props.bounds}
        controlPosition={google.maps.ControlPosition.TOP_LEFT}
        onPlacesChanged={props.onPlacesChanged}
        inputClassName={"u-map-search-box"}
        inputPlaceholder="Search"
      />

      {props.markers.map((marker, index) => (
        <Marker 
          position={marker.position}
          animation={marker.animation}
          key={"marker-" + index}
        />
      ))}

      {props.travelPlaces.map((travelPlace, index) => (
        <Marker 
          position={travelPlace.position}
          icon={travelPlace.icon}
          animation={travelPlace.animation}
          key={"travel-place-" + index}
        />
      ))}
    </GoogleMap>
  )
));

export default class TravelMap extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      bounds: null,
      center: { lat: 0, lng: 0 },
      markers: [],
      places: [],
      travelPlaces: [],
      travelDirections: []
    };

    this.handleMapMounted = this.handleMapMounted.bind(this);
    this.handleBoundsChanged = this.handleBoundsChanged.bind(this);
    this.handleSearchBoxMounted = this.handleSearchBoxMounted.bind(this);
    this.handlePlacesChanged = this.handlePlacesChanged.bind(this);
    this.handlePlaceClicked = this.handlePlaceClicked.bind(this);
    this.handleWannaGoClicked = this.handleWannaGoClicked.bind(this);
  }

  componentDidMount() {
    // const that = this;
    // if (navigator.geolocation) {
    //   navigator.geolocation.getCurrentPosition(function(position) {
    //     that.setState({
    //       center: {
    //         lat: position.coords.latitude,
    //         lng: position.coords.longitude
    //       }
    //     });
    //   }, function() {
    //     console.log();
    //   });
    // } else {
    //   console.log();
    // }


  }

  handleMapMounted(map) {
    this._map = map;

    const travelPlaces = [];
    http.get(this.props.urlGetTravelPlaces)
      .then(res => {
        console.log(res.data);
        res.data.map(data => {
          travelPlaces.push({
            name: data.fields.name,
            icon: {
              url: data.fields.icon,
              size: new google.maps.Size(71, 71),
              anchor: new google.maps.Point(10, 10),
              scaledSize: new google.maps.Size(20, 20)
            },
            type: data.fields.type,
            address: data.fields.address,
            position: {
              lat: parseFloat(data.fields.latitude),
              lng: parseFloat(data.fields.longitude)
            },
            animation: null
          });
        });

        this.setState({
          travelPlaces: travelPlaces
        });
      });
  }

  handleBoundsChanged() {
    this.setState({
      bounds: this._map.getBounds(),
      center: this._map.getCenter(),
    });
  }

  handleSearchBoxMounted(searchBox) {
    this._searchBox = searchBox;
  }

  handlePlacesChanged() {
    const places = this._searchBox.getPlaces();

    // Add a marker for each place returned from search bar
    const markers = places.map(place => ({
      position: place.geometry.location,
    }));

    // Set markers; set map center to first search result
    const center = markers.length > 0 ? markers[0].position : this.state.center;

    this.setState({
      center: center,
      places: places,
      markers: markers
    });
  }

  handlePlaceClicked(index, place) {
    this.state.markers.map(marker => {
      marker.animation = null;
    });
    const marker = this.state.markers[index];

    marker.animation = google.maps.Animation.BOUNCE;

    this.setState({
      markers: this.state.markers,
      center: marker.position
    });
  }

  handleWannaGoClicked(index, place) {
    console.log(this.props.urlAddWannaGo);
    http.post(this.props.urlAddWannaGo, {
      name: place.name,
      latitude: place.geometry.location.lat(),
      longitude: place.geometry.location.lng(),
      icon: place.icon,
      type: place.types[0],
      address: place.formatted_address
    })
      .then(res => {
        
      });
  }

  render() {
    return (
      <div>
        <div className={"col-md-9"}>
          <TravelGoogleMap
            googleMapURL="https://maps.googleapis.com/maps/api/js?key=AIzaSyBugTMDBzfPaBL0s_ORrXS2a5Zukjy1WR8&libraries=places"
            loadingElement={
              <div style={{ height: `100%` }}>
                Loading...
              </div>
            }
            containerElement={
              <div style={{ height: `100%` }} />
            }
            mapElement={
              <div style={{ height: `100%` }} />
            }
            center={this.state.center}
            bounds={this.state.bounds}
            markers={this.state.markers}
            travelPlaces={this.state.travelPlaces}
            travelDirections={this.state.travelDirections}

            onMapMounted={this.handleMapMounted}
            onBoundsChanged={this.handleBoundsChanged}
            onSearchBoxMounted={this.handleSearchBoxMounted}
            onPlacesChanged={this.handlePlacesChanged}
          >
          </TravelGoogleMap>
        </div>
        <div className={"col-md-3"}>
          <ul>
            {this.state.travelPlaces.map((place, index) => (
              <li key={"travel-place-" + index}>
                {place.name}
              </li>
            ))}
          </ul>
          <ul className="m-map-place-list">
            {this.state.places.map((place, index) => (
              <li 
                onClick={() => this.handlePlaceClicked(index, place)} 
                key={"place-" + index}
                >
                <div className="col-md-8">
                  <h4 className="name">
                    <img className="icon" src={place.icon} />
                    {place.name}
                  </h4>
                  <p className="address">{place.formatted_address}</p>
                  <button 
                    onClick={() => this.handleWannaGoClicked(index, place)}
                    className={"btn btn-default btn-sm"}
                  >Wanna go</button>
                </div>
                <div className="col-md-4">
                  <div className="photo" style={{backgroundImage: "url(" + 
                    (place.photos && place.photos.length > 0 ? 
                      place.photos[0].getUrl({
                        maxWidth: 176,
                        maxHeight: 176
                      }) : 
                      '') + ")"}}
                  />
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    );
  }
}
