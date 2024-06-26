<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <RouterLink class="navbar-brand" to="/">Navbar</RouterLink>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
        <li class="nav-item active">
            <RouterLink to="/" class="nav-link">Home <span class="sr-only">(current)</span></RouterLink>
        </li>
        <li class="nav-item">
            <RouterLink class="nav-link" to="/login" >Log In</RouterLink>
        </li>
        <li class="nav-item">
            <RouterLink class="nav-link" to="/login" >Register</RouterLink>
        </li>
        </ul>
        <form class="form-inline my-2 my-lg-0">
        <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
        <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
        </form>
    </div>
  </nav>
  {{  writings  }}
  {{ user_info }}
</template>

<script>
import axios from 'axios';
export default {
    name: "Navbar",
    data() {
        return {
            writings: '',
            user_info: ''
        };
    },
    methods: {
        getMessage() {
            const path = 'h';
            axios.get(path).then((res) => {
                this.msg = res.data;
            }).catch((error) => {
                console.error(error);
            });
        },
    },
    created() {
        this.getMessage();
    },
};
</script>