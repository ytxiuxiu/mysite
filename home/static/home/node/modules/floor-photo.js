import React from 'react';
import http from './http';

import layoutGeometry from 'justified-layout';
import Measure from 'react-measure';


const FloorPhoto = React.createClass({
  getInitialState() {
    return {
      load: 'loading',
      photos: [],
      dimensions: {
        width: 0,
        height: 0
      }
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
  render() {
    const SPACING = 14;
    const NAME_HEIGHT = 30;

    const container = {
      height: 0,
      width: this.state.dimensions.width - SPACING
    }

    const sizes = [];
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
        <Measure onMeasure={(dimensions) => {
            this.state.dimensions = dimensions;
            this.setState(this.state);
          }}>
          <div 
            className="m-floor m-floor-photo col-md-12" 
            style={{height: container.height + 'px'}}
            >
            {photos.map(photo =>
              <a href={photo.link}
                target="_blank"
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
      )
    }
  }
});

module.exports = FloorPhoto;