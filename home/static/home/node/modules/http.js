import axios from 'axios';

axios.defaults.headers = {'X-Requested-With': 'XMLHttpRequest'};

export default axios;