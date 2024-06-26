<template>
    <div class="home">
        {{ $route.params.username }}
        <p>{{ $route.params.id }}</p>
    </div>
</template>

<script>
export default {
    name: 'WritingView'
}
</script>