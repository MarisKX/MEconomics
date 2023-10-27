<template>
  <div class="home">
    <TopNav />
    <hr class="top-data-seperator" />
    <DataRow />
    <hr class="top-data-seperator" />
    <div class="main">
      <div v-if="companyDetails" class="my-5">
        <div class="row">
          <div class="col-6"><h4>General Data</h4></div>
          <div class="col-6">Stats</div>
        </div>
        <div class="row">
          <div class="col-6">
            <div class="row">
              <div class="col-6">Name:</div>
              <div class="col-6">
                {{ companyDetails.name }}
              </div>
            </div>
            <div class="row">
              <div class="col-6">Registration Number:</div>
              <div class="col-6">
                {{ companyDetails.registration_number }}
              </div>
            </div>
            <div class="row">
              <div class="col-6">Owner Type:</div>
              <div class="col-6">
                {{ companyDetails.owner_type }}
              </div>
            </div>
            <div class="row">
              <div class="col-6">Owner:</div>
              <div class="col-6">
                {{ companyDetails.owner_name }}
              </div>
            </div>
            <div class="row">
              <div class="col-6">Established:</div>
              <div class="col-6">
                {{ companyDetails.established }}
              </div>
            </div>
            <div class="row">
              <div class="col-6">Invoice Prefix:</div>
              <div class="col-6">
                {{ companyDetails.invoice_prefix }}
              </div>
            </div>
            <div class="row">
              <div class="col-6">Warehouse:</div>
              <div class="col-6">
                <span v-if="companyDetails.warehouse"
                  ><i class="fa-solid fa-check" style="color: #28b701"></i
                ></span>
                <span v-else
                  ><i class="fa-solid fa-xmark" style="color: #ff0000"></i
                ></span>
              </div>
            </div>
            <div class="row">
              <div class="col-6">Manufacturer Code:</div>
              <div class="col-6">
                {{ companyDetails.manufacturer_code }}
              </div>
            </div>
          </div>
          <div class="col-6">
            <div class="row">
              <div class="col-5">Employees Count:</div>
              <div class="col-3 text-end">
                {{ companyDetails.employee_count }}
              </div>
            </div>
            <div class="row">
              <div class="col-5">Total Cost of Salaries, Eur:</div>
              <div class="col-3 text-end">
                {{ companyDetails.total_salaries_cost }}
              </div>
            </div>
            <div class="row">
              <div class="col-5">Total Salaries Brutto, Eur:</div>
              <div class="col-3 text-end">
                {{ companyDetails.total_bruto_salaries }}
              </div>
            </div>
            <div class="row">
              <div class="col-5">Total VSAOI of Salaries (DD), Eur:</div>
              <div class="col-3 text-end">
                {{ companyDetails.total_salary_vsaoi_dd }}
              </div>
            </div>
            <div class="row">
              <div class="col-5">Total VSAOI of Salaries (DN), Eur:</div>
              <div class="col-3 text-end">
                {{ companyDetails.total_salary_vsaoi_dn }}
              </div>
            </div>
            <div class="row">
              <div class="col-5">Total IIN of Salaries, Eur:</div>
              <div class="col-3 text-end">
                {{ companyDetails.total_salary_iin }}
              </div>
            </div>
            <div class="row">
              <div class="col-5">Total Salaries Netto, Eur:</div>
              <div class="col-3 text-end">
                {{ companyDetails.total_salary_netto }}
              </div>
            </div>
            <div class="row">
              <div class="col-5">Average Salary Brutto, Eur:</div>
              <div class="col-3 text-end">
                {{ companyDetails.average_salary_brutto }}
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-6"><h4>Adress</h4></div>
            <div class="col-6"></div>
          </div>
          <div class="row">
            <div class="col-6">
              <div class="row">
                <div class="col-6">Street Adress 1:</div>
                <div class="col-6">
                  <span v-if="companyDetails.street_adress_1 != 0">{{
                    companyDetails.street_adress_1
                  }}</span>
                  <span v-else> - </span>
                </div>
              </div>
              <div class="row">
                <div class="col-6">Street Adress 2:</div>
                <div class="col-6">{{ companyDetails.street_adress_2 }}</div>
              </div>
              <div class="row">
                <div class="col-6">City/Town:</div>
                <div class="col-6">{{ companyDetails.city }}</div>
              </div>
              <div class="row">
                <div class="col-6">Postal Code:</div>
                <div class="col-6">{{ companyDetails.post_code }}</div>
              </div>
              <div class="row">
                <div class="col-6">Country:</div>
                <div class="col-6">{{ companyDetails.country }}</div>
              </div>
            </div>
            <div class="col-6"></div>
            <div class="col-6"></div>
          </div>
        </div>
      </div>
      <div class="text-center">
        <h4>Employees:</h4>
      </div>

      <TableView
        :visibleColumns="visibleColumns"
        :items="employees"
        :detailsRouteName="'citizen-details'"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import TopNav from "../components/TopNav.vue";
import DataRow from "../components/DataRow.vue";
import TableView from "../components/TableView.vue";
export default {
  name: "CompanyDetailsView",
  components: {
    TopNav,
    DataRow,
    TableView,
  },
  props: {
    id: {
      type: [String, Number],
      required: true,
    },
  },
  data() {
    return {
      companyDetails: null,
      columns: [],
      employees: [],
      showTooltip: false,
      showModal: false,
    };
  },
  computed: {
    visibleColumns() {
      return this.columns.slice(1);
    },
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get(
          "https://meconomics.com:8000/api/company/companies/" + this.id,
          {
            headers: {
              "X-CSRFToken": this.csrfToken,
            },
          }
        );

        console.log(response.data);
        this.companyDetails = response.data;
        console.log(this.companyDetails.name);

        // Check if the company has employees
        if (response.data.employees && response.data.employees.length > 0) {
          const firstEmployee = response.data.employees[0];
          this.columns = Object.keys(firstEmployee).map((key) => ({
            label: key.replace(/_/g, " ").toUpperCase(),
            field: key,
            sortable: true,
          }));

          this.employees = response.data.employees;
        }
      } catch (error) {
        console.error(error);
      }
    },
    toggleModal() {
      this.showModal = !this.showModal;
    },
  },
};
</script>
