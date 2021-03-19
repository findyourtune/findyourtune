<template>
    <div>
      <b-container fluid>
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
 }
 </style>