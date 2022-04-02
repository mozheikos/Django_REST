import React from 'react';
import './App.css';
import UsersList from './components/Users';
import FooterInfo from './components/Footer';
import Menu from './components/Menu';
import Projects from "./components/Projects";
import Remarks from "./components/ToDo";
import ProjectDetail from "./components/ProjectDetail";
import {BrowserRouter, Redirect, Route} from "react-router-dom";
import axios from 'axios';

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'users': [],
            'projects': [],
            'remarks': [],
            'links': [
                {"verbose_name": "Все пользователи", "link": "/users"},
                {"verbose_name": "Проекты", "link": "/projects"},
                {"verbose_name": "TODO-листы", "link": "/ToDo"},
            ],
        };
    }

    componentDidMount() {
        axios.get(
            'http://127.0.0.1:8000/api/users'
        ).then(
            response => {
                const users = response.data.results;
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
            'http://127.0.0.1:8000/api/ToDo'
        ).then(
            response => {
              const remarks = response.data.results;
              this.setState(
                  {
                      'remarks': remarks,
                  }
              );
            }
        ).catch(
            error => console.log(error)
        );
        axios.get(
            'http://127.0.0.1:8000/api/projects'
        ).then(
            response => {
              const projects = response.data.results;
              this.setState(
                  {
                      'projects': projects,
                  }
              );
            }
        ).catch(
            error => console.log(error)
        );
    }

    render() {
        return (

            <div className="table">
                <BrowserRouter>
                    < Menu links={this.state.links}/>
                    <Route exact path={'/users'} component={() => < UsersList users={this.state.users}/>}/>
                    <Route exact path={'/projects'} component={() => < Projects projects={this.state.projects} users={this.state.users}/>}/>
                    <Route path={"/projects/:id"}>
                            < ProjectDetail projects={this.state.projects} users={this.state.users}/>
                    </Route>
                    <Route exact path={'/ToDo'}>
                        < Remarks remarks={this.state.remarks} />
                    </Route>
                </BrowserRouter>
                    < FooterInfo />
            </div>
        )
    };
}
export default App;
