<template>
  <div>
    <img src="static/pic1.png" style="width: 600px; height: 400px">
    <div>This is a automatic lyrics generator. That could generate lyrics with one starting character.</div>
    <div>Example: Input 'h', You could get the following lyrics:</div>
    <div class="ui large input">
      <input type="text" v-model="word" placeholder="Input one word">
      <button class="ui button" @click="sendWord()">Generate</button>
    </div>
    <div class="ui segment" style="width: 800px; height: 600px; margin: 10px auto 0 auto">
      <div :class="[activeClass, invertClass]">
        <div class="ui text loader">{{lyrics}}</div>
      </div>
      <p></p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data() {
    return {
      activeClass: '',
      invertClass: 'ui inverted dimmer',
      word: '',
      lyrics: '',
      url: 'http://localhost:5000/generate'
    }
  },
  methods: {
    sendWord() {
      this.lyrics = 'Loading...'
      this.activeClass = 'active'
      this.axios
        .post(this.url, { word: this.word, description: 'for generating' })
        .then(res => {
          this.lyrics = res.data.lyrics
          console.log(res.data)
          this.activeClass = ''
        })
        .catch(function(e) {
          console.log(e)
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
