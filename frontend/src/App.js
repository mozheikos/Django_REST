import React from 'react';
import './App.css';
import UsersList from './components/Users';
import FooterInfo from './components/Footer';
import Menu from './components/Menu';
import Projects from "./components/Projects";
import Remarks from "./components/ToDo";
import ProjectDetail from "./components/ProjectDetail";
import UserDetail from "./components/UserDetail";
import LoginButton from "./components/LoginButton";
import LoginComponent from "./components/LoginComponent";
import ProjectCreate from "./components/ProjectCreate";
import ProjectUpdate from "./components/ProjectUpdate";
import {BrowserRouter, Route, Redirect} from "react-router-dom";
import axios from 'axios';
import Cookies from "universal-cookie/es6";
import jwt_decode from "jwt-decode";
import ToDOCreate from "./components/ToDOCreate";
import Forbidden from "./components/Forbidden";


class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'users': [],
            'users_page': 1,
            'users_pages': null,
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
            'access_token': '',
            'refresh_token': '',
            'user': null,
            'links': [
                {"verbose_name": "Все пользователи", "link": "/users"},
                {"verbose_name": "Проекты", "link": "/projects"},
                {"verbose_name": "TODO-листы", "link": "/ToDo"},
            ],
        };
    }
    get_content(){
        let headers;
        if (this.is_authenticated()) {
            headers = this.get_headers()
        }
        axios.get(
            `http://127.0.0.1:8000/api/users/`,
            {headers}).then(
            response => {
                const users = response.data;
                const pages = Math.ceil(response.data.length / this.state.users_limit);
                this.setState(
                    {
                        'users': users,
                        'users_pages': pages,
                    }
                );
            }
        ).catch(
            error => {
                console.log(error);
            }
        );
        axios.get(
            `http://127.0.0.1:8000/api/ToDo/?offset=0&limit=${this.state.remarks_limit}`,
        {headers}).then(
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
            error => {console.log(error);
            }
        );
        axios.get(
            `http://127.0.0.1:8000/api/projects/?offset=0&limit=${this.state.projects_limit}`,
        {headers}).then(
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
            error => {
                console.dir(error);
            }
        );
    }

    get_headers() {
        return {
            "Authorization": `Bearer ${this.state.access_token}`,
            "Content-Type": "application/json"
        }
    }

    is_authenticated() {
        return !!this.state.access_token
    }

    componentDidMount() {
        this.get_cookie();
        this.get_user_from_token();
        this.get_content();
    }

    refresh_token(){
        axios.post("http://127.0.0.1:8000/api/jwt-token/refresh/", {"refresh": this.state.refresh_token}
        ).then(response => {
            const access = response.data.access;
            const refresh = response.data.refresh;
            this.setState({
                "access_token": access,
                "refresh_token": refresh
            })
        }).catch(error => console.dir(error));
        this.set_cookie();
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (prevState.access_token !== this.state.access_token){
            this.setState({
                'users_page': 1,
                'projects_page': 1,
                'remarks_page': 1,
                'users_offset': 0,
                'projects_offset': 0,
                'remarks_offset': 0,
                'users': [],
                'projects': [],
                'remarks': [],
            })
            this.get_content();
            this.get_user_from_token();
        }
        let headers;
        if (this.is_authenticated()){
            headers = this.get_headers();
        }
        // if (prevState.users_offset < this.state.users_offset) {
        //     axios.get(
        //         `http://127.0.0.1:8000/api/users/?offset=${this.state.users_offset}&limit=${this.state.users_limit}`,
        //         {headers}).then(response => {
        //         const users = this.state.users;
        //         users.push(...response.data.results)
        //         this.setState(
        //             {
        //                 'users': users
        //             }
        //         );
        //     }).catch(
        //         error => {
        //             console.log(error);
        //         }
        //     );
        // }
        if (prevState.projects_offset < this.state.projects_offset) {
            axios.get(
                `http://127.0.0.1:8000/api/projects/?offset=${this.state.projects_offset}&limit=${this.state.projects_limit}`,
            {headers}).then(response => {
                const projects = this.state.projects;
                projects.push(...response.data.results)
                this.setState(
                    {
                        'projects': projects
                    }
                )
            }).catch(
                error => {
                    console.log(error);
                }
            );
        }
        if (prevState.remarks_offset < this.state.remarks_offset) {
            axios.get(
                `http://127.0.0.1:8000/api/ToDo/?offset=${this.state.remarks_offset}&limit=${this.state.remarks_limit}`,
            {headers}).then(response => {
                const remarks = this.state.remarks;
                remarks.push(...response.data.results)
                this.setState(
                    {
                        'remarks': remarks
                    }
                )
            }).catch(
                error => {
                    console.log(error);
                }
            );
        }
    }

    get_cookie() {
        const cookie = new Cookies();
            let access = cookie.get('access');
            let refresh = cookie.get('refresh');
            this.setState({
                "access_token": access,
                "refresh_token": refresh
            })
    }

    set_cookie() {
        const cookie = new Cookies();
        const access_exp = jwt_decode(this.state.access_token).exp;
        const refresh_exp = jwt_decode(this.state.refresh_token).exp;
        let access_exp_data = new Date(access_exp * 1000);
        let refresh_exp_data = new Date(refresh_exp * 1000);
        let options_access = {"expires": access_exp_data};
        let options_refresh = {"expires": refresh_exp_data};
        let options_user = {"expires": access_exp_data};

        cookie.set('access', this.state.access_token, options_access);
        cookie.set('refresh', this.state.refresh_token, options_refresh);
        cookie.set('user', this.state.user, options_user);
    }

    get_user_from_token() {
        let token = this.state.access_token;
        if (token) {
            const user = jwt_decode(token).user_id;
            let headers;
            if (this.is_authenticated()) {
                headers = this.get_headers()
            }
            axios.get(`http://127.0.0.1:8000/api/users/${user}`, {headers}).then(
                response => {
                    this.setState({
                        "user": response.data
                    })
                }
            ).catch(error => console.log(error))
        }
    }

    get_access(username, password) {
        axios.post("http://localhost:8000/api/jwt-token/", {"username": username,
            "password": password}).then(response => {
                const access = response.data.access;
                const refresh = response.data.refresh;
                this.setState({
                    "access_token": access,
                    "refresh_token": refresh,
                });
                this.set_cookie();
                this.get_user_from_token();
                this.get_content();
        }).catch(error => console.dir(error));
    }

    set_credentials(username, password) {
        this.get_access(username, password);
    }

    logout() {
        const cookie = new Cookies();
        cookie.remove("access");
        cookie.remove("refresh");
        cookie.remove("user");
        this.setState({
            'access_token': '',
            'refresh_token': '',
            'user': null,
        })
    }

    create_project(data) {
        const headers = this.get_headers()
        axios.post('http://127.0.0.1:8000/api/projects/', data, {headers}
        ).then(response => {
                const projects = this.state.projects;
                let pages = this.state.projects_pages;
                projects.push(response.data);
                let new_pages = Math.ceil(projects.length / this.state.projects_limit);
                if ( new_pages > pages ){
                    pages = new_pages
                }
                this.setState({
                    'projects': projects,
                    'projects_pages': pages
                });
            }
        ).catch(error => console.log(error))
    }

    delete_project(id) {
        const headers = this.get_headers();
        axios.delete(`http://127.0.0.1:8000/api/projects/${id}/`, {headers}
        ).then(
            response => {
                console.dir(this.state);
                const projects = this.state.projects.filter(project => project.id !== id);
                const pages = Math.ceil(projects.length / this.state.projects_limit);
                console.log(pages);
                let new_page = this.state.projects_page;
                let new_pages = this.state.projects_pages;
                if (pages < new_pages) {
                    new_pages = pages
                }
                if (new_page > new_pages) {
                    new_page = new_pages
                }
                this.setState({
                    'projects': projects,
                    'projects_page': new_page,
                    'projects_pages': new_pages
                });
                console.dir(this.state)
            }
        ).catch(error => console.log(error))
    }

    find_project(name) {
        this.setState({
            'projects_page': 1,
            'projects_pages': null,
            'projects_offset': 0,
            'projects': [],
        });
        axios.get(`http://127.0.0.1:8000/api/projects/?title=${name}&users=`
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
        ).catch(error => console.log(error))
    }

    update_project(id, data) {
        const headers = this.get_headers();
        axios.put(`http://localhost:8000/api/projects/${id}/`, data, {headers}
        ).then(
            response => {
                let new_project = response.data;
                let projects = this.state.projects;
                let idx = projects.findIndex(project => project.id === new_project.id);
                projects.splice(idx, 1, new_project)
                this.setState({
                    "projects": projects
                })
            }
        ).catch(
            error => console.log(error)
        )
    }

    create_remark(data) {
        const headers = this.get_headers()
        console.dir(data);
        axios.post('http://127.0.0.1:8000/api/ToDo/', data, {headers}
        ).then(response => {
                const remarks = this.state.remarks;
                let pages = this.state.remarks_pages;
                remarks.push(response.data);
                let new_pages = Math.ceil(remarks.length / this.state.remarks_limit);
                if ( new_pages > pages ){
                    pages = new_pages
                }
                this.setState({
                    'remarks': remarks,
                    'remarks_pages': pages
                });
            }
        ).catch(error => console.log(error))
    }

    delete_remark(id) {
        const headers = this.get_headers();
        axios.delete(`http://127.0.0.1:8000/api/ToDo/${id}/`, {headers}
        ).then(
            response => {
                this.setState({
                    "remarks": [],
                });
                axios.get(`http://127.0.0.1:8000/api/ToDo/?offset=0&limit=${this.state.remarks_limit * this.state.remarks_pages}`
                ).then(
                    response => {
                        this.setState({
                            "remarks": response.data.results
                        })
                    }
                ).catch(
                    error => console.log(error)
                )
            }
        ).catch(error => console.log(error))
    }

    render() {
        return (

            <div className="table">
                <BrowserRouter>
                    < Menu links={this.state.links}/>
                    < LoginButton user={this.state.user} App={this}/>
                    <Route exact path={"/login"} component={() => <LoginComponent get_token={(username, password) => this.set_credentials(username, password)}/>}/>
                    <Route exact path={'/users'} component={() => < UsersList App={this} users={this.state.users}/>}/>
                    <Route exact path={'/projects'} component={() =>
                        this.is_authenticated() ? < Projects App={this} projects={this.state.projects} users={this.state.users}/>
                                                : <LoginComponent get_token={(username, password) => this.set_credentials(username, password)}/>}/>
                    <Route exact path={"/project/create"} component={() =>
                        this.is_authenticated() ? <ProjectCreate App={this} />
                                                : <LoginComponent get_token={(username, password) => this.set_credentials(username, password)}/>}/>
                    <Route path={"/project/update/:id"} component={() =>
                        this.is_authenticated() ? <ProjectUpdate App={this} />
                                                : <LoginComponent get_token={(username, password) => this.set_credentials(username, password)}/>}/>
                    <Route path={"/projects/:id"}>
                            < ProjectDetail projects={this.state.projects} users={this.state.users}/>
                    </Route>

                    <Route path={"/users/:id"}>
                            < UserDetail users={this.state.users} projects={this.state.projects} />
                    </Route>
                    <Route exact path={'/ToDo'}>
                        < Remarks App={this} remarks={this.state.remarks} users={this.state.users}/>
                    </Route>
                    <Route exact path={"/ToDo/create"} component={() =>
                        this.is_authenticated() ? <ToDOCreate App={this}/>
                                                : <LoginComponent get_token={(username, password) => this.set_credentials(username, password)}/>}/>
                </BrowserRouter>
                    < FooterInfo />
            </div>
        )
    };
}
export default App;
