import React, {Component} from 'react';
import { Header, Divider, Segment, Card, Container, Input, List, Statistic } from 'semantic-ui-react';
import getUserData from '../actions/actions.js';
import SpotifyPlayer from 'react-spotify-player';


class MainPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            user_id: null,
            song_metadata: null,
            heart_rate: null
        }
    }

    getUserDataFromForm = () => {
        if (!(this.state.user_id)) {
            return;
        }
        getUserData(this.state.user_id, (res, err) => {
            if (err) {
                console.log(err);
                return;
            }
            this.setState({
                song_metadata: res.track_list,
                heart_rate: res.heart_rate
            });
        });
    }

    handleUserIDChange = (src) => {
        this.setState({user_id: src.target.value});
    }

    render() {
        let song_list = null;
        if (this.state.song_metadata) {
            song_list = this.state.song_metadata.map((item, index) => {
                return (
                    <List.Item key={index}>
                        <SpotifyPlayer uri={item} size={"large"} view={"coverart"} theme={"black"} />
                    </List.Item>
                )
            })
        }
        return (
            <Segment raised>
                <Header as="h1">Musiquity</Header>
                <Input action={{color: 'blue', labelPosition: 'right', icon: 'plus', content: 'Get data for user', onClick: this.getUserDataFromForm.bind(this)}}
                       placeholder='Enter username...' value={this.state.user_id} onChange={this.handleUserIDChange.bind(this)} />
                <Divider></Divider>
                <div align="center">
                    {this.state.heart_rate ? 
                    <Card color="olive">
                    <Statistic>
                        <Statistic.Value>
                        {this.state.heart_rate}
                        </Statistic.Value>
                        <Divider> 
                        </Divider>
                        <Statistic.Label>Current Heart Rate</Statistic.Label>
                    </Statistic>
                    </Card> : null }
                </div>
                
                {this.state.song_metadata ? <List horizontal divided relaxed>{song_list}</List> : null}
            </Segment>
        )
    }
}

export default MainPage;