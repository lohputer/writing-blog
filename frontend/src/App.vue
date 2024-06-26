<template>
  
  <router-view/>
</template>

<style>
#app {
  font-family: "Playfair Display", serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav RouterLink {
  font-weight: bold;
  color: #2c3e50;
}

nav RouterLink.router-link-exact-active {
  color: #42b983;
}
</style>
