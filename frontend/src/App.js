import React from 'react';
import './App.css';
import UsersList from './components/Users';
import FooterInfo from './components/Footer';
import Menu from './components/Menu';
import Projects from "./components/Projects";
import Remarks from "./components/ToDo";
import ProjectDetail from "./components/ProjectDetail";
import UserDetail from "./components/UserDetail";
import {BrowserRouter, Route} from "react-router-dom";
import axios from 'axios';


class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'users': [],
            'users_page': 1,
            "users_pages": null,
            'users_offset': 0,
            'users_limit': 100,
            'projects': [],
            'projects_page': 1,
            'projects_pages': null,
            'projects_offset': 0,
            'projects_limit': 10,
            'remarks': [],
            'remarks_page': 1,
            'remarks_pages': null,
            'remarks_offset': 0,
            'remarks_limit': 2,
            'links': [
                {"verbose_name": "Все пользователи", "link": "/users"},
                {"verbose_name": "Проекты", "link": "/projects"},
                {"verbose_name": "TODO-листы", "link": "/ToDo"},
            ],
        };
    }

    componentDidMount() {
        axios.get(
            `http://127.0.0.1:8000/api/users/?offset=${this.state.users_offset}&limit=${this.state.users_limit}`
        ).then(
            response => {
                const users = response.data.results;
                const pages = Math.ceil(response.data.count / this.state.users_limit);
                this.setState(
                    {
                        'users': users,
                        'users_pages': pages,

                    }
                );
            }
        ).catch(
            error => console.log(error)
        );
        axios.get(
            `http://127.0.0.1:8000/api/ToDo/?offset=${this.state.remarks_offset}&limit=${this.state.remarks_limit}`
        ).then(
            response => {
              const remarks = response.data.results;
              const pages = Math.ceil(response.data.count / this.state.remarks_limit);
              this.setState(
                  {
                      'remarks': remarks,
                      "remarks_pages": pages
                  }
              );
            }
        ).catch(
            error => console.log(error)
        );
        axios.get(
            `http://127.0.0.1:8000/api/projects/?offset=${this.state.projects_offset}&limit=${this.state.projects_limit}`
        ).then(
            response => {
              const projects = response.data.results;
              const pages = Math.ceil(response.data.count / this.state.projects_limit);
              this.setState(
                  {
                      'projects': projects,
                      'projects_pages': pages
                  }
              );
            }
        ).catch(
            error => console.log(error)
        );
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (prevState.users_offset < this.state.users_offset) {
            axios.get(
                `http://127.0.0.1:8000/api/users/?offset=${this.state.users_offset}&limit=${this.state.users_limit}`
            ).then(response => {
                const users = this.state.users;
                users.push(...response.data.results)
                this.setState(
                    {
                        'users': users
                    }
                )
            }).catch(
                error => console.log(error)
            );
        }
        if (prevState.projects_offset < this.state.projects_offset) {
            axios.get(
                `http://127.0.0.1:8000/api/projects/?offset=${this.state.projects_offset}&limit=${this.state.projects_limit}`
            ).then(response => {
                const projects = this.state.projects;
                projects.push(...response.data.results)
                this.setState(
                    {
                        'projects': projects
                    }
                )
            }).catch(
                error => console.log(error)
            );
        }
        if (prevState.remarks_offset < this.state.remarks_offset) {
            axios.get(
                `http://127.0.0.1:8000/api/ToDo/?offset=${this.state.remarks_offset}&limit=${this.state.remarks_limit}`
            ).then(response => {
                const remarks = this.state.remarks;
                remarks.push(...response.data.results)
                this.setState(
                    {
                        'remarks': remarks
                    }
                )
            }).catch(
                error => console.log(error)
            );
        }
    }

    render() {
        return (

            <div className="table">
                <BrowserRouter>
                    < Menu links={this.state.links}/>
                    <Route exact path={'/users'} component={() => < UsersList App={this} users={this.state.users}/>}/>
                    <Route exact path={'/projects'} component={() => < Projects App={this} projects={this.state.projects} users={this.state.users}/>}/>
                    <Route path={"/projects/:id"}>
                            < ProjectDetail projects={this.state.projects} users={this.state.users}/>
                    </Route>
                    <Route path={"/users/:id"}>
                            < UserDetail users={this.state.users} projects={this.state.projects} />
                    </Route>
                    <Route exact path={'/ToDo'}>
                        < Remarks App={this} remarks={this.state.remarks} users={this.state.users}/>
                    </Route>
                </BrowserRouter>
                    < FooterInfo />
            </div>
        )
    };
}
export default App;
