<template>
  <div class="container d-flex align-items-center py-2 my-2">
    <div class="row w-100">
      <div
        class="col-12 col-lg-4 my-auto py-1 py-lg-0 text-center text-lg-left"
      >
        <router-link to="/" class="nav-link main-logo-link"
          ><h2 class="logo-font my-0 text-green">M Economics</h2></router-link
        >
      </div>
      <div
        class="col-12 col-lg-8 my-auto py-1 py-lg-0 text-center text-lg-left"
      >
        <div class="d-flex">
          <!-- Use d-flex class to create a flex container -->
          <div class="dropdown mx-2">
            <button
              class="btn btn-secondary bg-green dropdown-toggle"
              type="button"
              id="invoicesDropdown"
              data-bs-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
            >
              Invoices
            </button>
            <div class="dropdown-menu" aria-labelledby="invoicesDropdown">
              <router-link to="/" class="dropdown-item"
                >New Invoice</router-link
              >
              <router-link to="/" class="dropdown-item"
                >All Invoices</router-link
              >
              <div class="dropdown-divider"></div>
            </div>
          </div>
          <div class="dropdown mx-2">
            <button
              class="btn btn-secondary bg-green dropdown-toggle"
              type="button"
              id="citizensDropdown"
              data-bs-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
            >
              Persons
            </button>
            <div class="dropdown-menu" aria-labelledby="citizensDropdown">
              <router-link to="/companies" class="dropdown-item"
                >Companies</router-link
              >
              <router-link to="/citizens" class="dropdown-item"
                >Citizens</router-link
              >
              <router-link to="/government" class="dropdown-item"
                >Government</router-link
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script></script>

<style>
.dropdown-toggle::after {
  display: none !important;
}
</style>
