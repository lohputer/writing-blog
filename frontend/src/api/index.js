import axios from 'axios'

const API_URL = 'http://127.0.0.1:5000/'

export function fetchWritings() {
    return axios.get(`${API_URL}/`)
}

export function searchWritings(text) {
    return axios.get(`${API_URL}/search/${text}`)
}

export function fetchProfile(username) {
    return axios.get(`${API_URL}/users/${username}`)
}

export function publishWriting(writingData) {
    return axios.post(`${API_URL}/publish`, writingData)
}