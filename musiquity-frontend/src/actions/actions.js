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


export default getUserData;