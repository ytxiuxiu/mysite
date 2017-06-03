import React from 'react';
import http from './http';

import layoutGeometry from 'justified-layout';
import Measure from 'react-measure';

// left: 37, up: 38, right: 39, down: 40,
// spacebar: 32, pageup: 33, pagedown: 34, end: 35, home: 36
var keys = {37: 1, 38: 1, 39: 1, 40: 1};

function preventDefault(e) {
  e = e || window.event;
  if (e.preventDefault)
      e.preventDefault();
  e.returnValue = false;  
}

function preventDefaultForScrollKeys(e) {
    if (keys[e.keyCode]) {
        preventDefault(e);
        return false;
    }
}

function disableScroll() {
  if (window.addEventListener) // older FF
      window.addEventListener('DOMMouseScroll', preventDefault, false);
  window.onwheel = preventDefault; // modern standard
  window.onmousewheel = document.onmousewheel = preventDefault; // older browsers, IE
  window.ontouchmove  = preventDefault; // mobile
  document.onkeydown  = preventDefaultForScrollKeys;
}

function enableScroll() {
    if (window.removeEventListener)
        window.removeEventListener('DOMMouseScroll', preventDefault, false);
    window.onmousewheel = document.onmousewheel = null; 
    window.onwheel = null; 
    window.ontouchmove = null;  
    document.onkeydown = null;  
}


const FloorPhoto = React.createClass({
  getInitialState() {
    return {
      load: 'loading',
      photo: {
        state: 'hide',
        src: null
      },
      photos: [],
      dimensions: {
        width: 0,
        height: 0
      },
    };
  },
  componentDidMount() {
    http.get(this.props.url)
      .then(res => {
        this.setState({
          photos: res.data,
          load: 'loaded'
        });
      });
  },
  photoClicked(clickedPhoto) {
    if (clickedPhoto.link) {
      window.location.href = clickedPhoto.link;
    } else {
      this.setState({
        photo: {
          state: 'show',
          src: clickedPhoto.fields.stylish_image_url ? 
              clickedPhoto.fields.stylish_image_url : 
              clickedPhoto.fields.original_image_url
        }
      });
      disableScroll();
    }
  },
  photoCloseClicked() {
    this.setState({
      photo: {
        state: 'hide'
      }
    });
    enableScroll();
  },
  render() {
    const SPACING = 14;
    const NAME_HEIGHT = 30;

    const container = {
      height: 0,
      width: this.state.dimensions.width - SPACING
    }

    const sizes = [];
    const photo = this.state.photo;
    const photos = this.state.photos;
    photos.map(photo => {
      sizes.push({
        width: photo.fields.image_size[0],
        height: photo.fields.image_size[1]
      });

      if (photo.model === 'home.page') {
        photo.link = '/' + photo.fields['category.link'] + '/' + photo.fields.link + '/';
      }
    });

    const layout = layoutGeometry(sizes, {
      containerPadding: 0,
      containerWidth: container.width,
      boxSpacing: SPACING,
      targetRowHeight: this.props.height ? this.props.height : 320
    });
    
    var lastTop = 0;
    var level = 0;
    for (var i = 0, l = layout.boxes.length; i < l; i++) {
      var box = layout.boxes[i];
      var level = box.top > lastTop ? level + 1 : level;
      photos[i].style = {
        transform: 'translate(' + box.left + 'px, ' + (box.top + level * NAME_HEIGHT) + 'px)',
        width: box.width + 'px', 
        height: (box.height + NAME_HEIGHT) + 'px'
      };
      lastTop = box.top;
    }
    container.height = layout.containerHeight + (level + 1) * NAME_HEIGHT;

    if (this.state.load === 'loading') {
      return (
        <div className="m-floor m-floor-photo col-md-12">
          Loading...
        </div>
      );
    } else if (this.state.load === 'loaded') {
      return (
        <div>
        <Measure onMeasure={(dimensions) => {
            this.state.dimensions = dimensions;
            this.setState(this.state);
          }}>
          <div 
            className="m-floor m-floor-photo col-md-12" 
            style={{height: container.height + 'px', cursor: 'pointer'}}
            >
            {photos.map(photo =>
              <a onClick={() => this.photoClicked(photo)}
                key={'p-' + photo.pk}>
                <div className="photo" 
                  style={photo.style}>
                  <img src={photo.fields.image_thumbnail}/>
                  <div className="name">
                    {photo.fields.name &&
                      <span>- {photo.fields.name} -</span>
                    }
                    {!photo.fields.name &&
                      <span>- Unnamed Guy -</span>
                    }
                  </div>
                </div>
              </a>
            )}
          </div>
        </Measure>
        { photo.state == 'show' ? 
          <div
            style={{cursor: 'pointer'}}
            onClick={this.photoCloseClicked} 
            className="m-view-photo-container"
            >
            <img src={photo.src}/>
          </div>
          :
          <div></div>
        }
        </div>
      )
    }
  }
});

module.exports = FloorPhoto;