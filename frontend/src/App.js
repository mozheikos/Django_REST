import React from 'react';
import logo from './logo.svg';
import './App.css';
import UsersList from './components/Users';
import FooterInfo from './components/Footer';
import Menu from './components/Menu';
import axios from 'axios';

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'users': [],
            'links': [],
        };
    }

    componentDidMount() {
        axios.get(
            'http://127.0.0.1:8000/api/users'
        ).then(
            response => {
                const users = response.data;
                this.setState(
                    {
                        'users': users,
                    }
                );
            }
        ).catch(
            error => console.log(error)
        );
        axios.get(
            'http://127.0.0.1:8000/api/links'
        ).then(
            response => {
              const links = response.data.links;
              this.setState(
                  {
                      'links': links,
                  }
              );
            }
        ).catch(
            error => console.log(error)
        );
    }

    render() {
        return (

            <div class="table">
                < Menu links={this.state.links} />
                < UsersList users={this.state.users} />
                < FooterInfo />
            </div>
        )
    };
}
export default App;
