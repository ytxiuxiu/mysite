import React from 'react';
import axios from 'axios';
import layoutGeometry from 'justified-layout';
import Measure from 'react-measure';

axios.defaults.headers = {'X-Requested-With': 'XMLHttpRequest'};


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
    axios.get(this.props.url)
      .then(res => {
        const photos = res.data;
        this.state.photos = photos;
        this.state.load = 'loaded';
        this.setState(this.state);
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
      console.log(level, box.top, box.top + level * NAME_HEIGHT);
      photos[i].style = {
        transform: 'translate(' + box.left + 'px, ' + (box.top + level * NAME_HEIGHT) + 'px)',
        width: box.width + 'px', 
        height: (box.height + NAME_HEIGHT) + 'px'
      };
      console.log(photos[i].style);
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
          <div className="m-floor m-floor-photo col-md-12" style={{height: container.height + 'px'}}>
            {photos.map(photo =>
              <div className="photo" 
                key={photo.pk}
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
            )}
          </div>
        </Measure>
      )
    }
  }
});

module.exports = FloorPhoto;