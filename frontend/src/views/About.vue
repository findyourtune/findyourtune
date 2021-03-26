<template>
    <div>
      <b-container fluid>
        <h1 class="about-page-title">Abstract</h1>
        <b-card class="mb-5">Findyourtune(FYT) is a social media application aimed towards music sharing and discovery. This
          application provides an intuitive way to discover, share and discuss music with friends and other likeminded individuals. The application connects to the users Spotify account, allowing easy access to music
          sharing.
        </b-card>

        <themed-divider></themed-divider>

        <h1 class="about-page-title">Project Video</h1>
        <span class="custom-link ml-5" @click="toExternalLink('https://drive.google.com/file/d/1Rn2PvFOye5MSn5QG6g-iB70yBHfsV1bO/view')"><b-icon icon="box-arrow-up-right" aria-hidden="true"></b-icon><span class="ml-1">Link</span></span>
        <iframe src="https://drive.google.com/file/d/1Rn2PvFOye5MSn5QG6g-iB70yBHfsV1bO/preview" width="640" height="480" ></iframe>

        <themed-divider></themed-divider>

        <h1 class="about-page-title">Project Poster</h1>
        <span class="custom-link ml-5" @click="toExternalLink('https://drive.google.com/file/d/1LC1MXXQHqTnPqJhnNNcRTJMjyzJ3V6aJ/view')"><b-icon icon="box-arrow-up-right" aria-hidden="true"></b-icon><span class="ml-1">Link</span></span>
        <img src="@/assets/posterScreenshot.png"/>

        <themed-divider></themed-divider>

        <h1 class="about-page-title">Team Members</h1>
        <b-card img-src="@/assets/matt.png" img-width="250" img-alt="Matthew Jackson" img-left class="mb-5">
          <b-card-text>
            <div class="member-name">Matthew Jackson</div>
            Matthew Jackson is a 5th year student at the University of Cincinnati graduating in 2021 with a Bachelor's Degree in Computer Engineering.
          </b-card-text>
        </b-card>
        
        <b-card img-src="@/assets/nathan.png" img-width="250" img-alt="Matthew Jackson" img-right class="mb-5">
          <b-card-text>
            <div class="member-name">Nathan Sucher</div>
            Nathan Sucher is a 5th year student at the University of Cincinnati graduating in 2021 with a Bachelor's Degree in Computer Engineering.
          </b-card-text>
        </b-card>

        <b-card img-src="@/assets/steve.png" img-width="250" img-alt="Matthew Jackson" img-left class="mb-5">
          <b-card-text>
            <div class="member-name">Stephen Comarata</div>
            Stephen Comarata is a 5th year student at the University of Cincinnati graduating in 2021 with a Bachelor's Degree in Computer Engineering.
          </b-card-text>
        </b-card>

        <b-card img-src="@/assets/dylan.png" img-width="250" img-alt="Matthew Jackson" img-right class="mb-5">
          <b-card-text>
            <div class="member-name">Dylan Wheeler</div>
            Dylan Wheeler is a 5th year student at the University of Cincinnati graduating in 2021 with a Bachelor's Degree in Computer Engineering.
          </b-card-text>
        </b-card>
      </b-container>
    </div>
</template>

<script>
 export default {
  name: 'About',
  methods: {
    toExternalLink(url) {
        window.open(url);
    }
  }
 };
 </script>

 <style scoped>
 .member-name {
    font-size: 1.7rem;
    font-weight: bold;
    margin-bottom: 5px;
 }
 .about-page-title {
   font-size: 2rem;
   margin-bottom: 15px;
   display: inline-block;
 }
 </style>