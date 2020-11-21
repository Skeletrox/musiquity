import axios from 'axios';


let getUserData = (user, cb) => {
    axios.get(`http://localhost:8000/data/get_tracks/${user}`).then(response => {
        let res = response.data;
        let returnable = res.returnable;
        cb(returnable);
    }).catch(err => {
        cb(null, err);
    });
}

let getUserCutoffData = (user, cb) => {
    axios.get(`http://localhost:8000/data/get_cutoffs/${user}`).then(response => {
        let res = response.data;
        let returnable = res.cutoffs;
        cb(returnable);
    }).catch(err => {
        cb(null, err);
    });
}

export { getUserData, getUserCutoffData };