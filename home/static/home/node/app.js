import React from 'react';
import { render } from 'react-dom';
import ReactHabitat from 'react-habitat';

import FloorPhoto from './modules/floor-photo.js';


class App extends ReactHabitat.Bootstrapper {
  constructor() {
    super();

    var container = new ReactHabitat.Container();

    container.registerAll({
      'floor-photo': FloorPhoto
    });

    this.setContainer(container);
  }
}

export default new App();