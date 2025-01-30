<template>

<div class="dropdown" v-click-outside="closeDropdown">
  <h4 :class="['nav-link', selected ? 'selected' : '']" @click="toggleSubmenu">{{ title }} <font-awesome-icon :icon="icon" /></h4>
  <transition name="slide">
    <div v-if="isOpen" :class="['submenu', isOpen ? 'open' : '' ]">
      <router-link v-for="(item, i) in items" :key="i" :to="{name: item.routerName}" @click.native="closeDropdown">{{ item.title }}</router-link>
    </div>
  </transition>
</div>

</template>

<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faCaretDown } from '@fortawesome/free-solid-svg-icons';
import { faCaretUp } from '@fortawesome/free-solid-svg-icons';

export default {
  name: 'DropDown',
  props: ['title', 'items'],
  data() {
    return {
      isOpen: false
    }
  },
  computed: {
    icon() {
      return this.isOpen ? faCaretUp : faCaretDown;
    },
    selected() {
      return this.items.some(item => item.routerName === this.$route.name);
    }
  },
  methods: {
    toggleSubmenu() {
      this.isOpen = !this.isOpen;
    },
    closeDropdown() {
      this.isOpen = false;
    }
  },
  components: { FontAwesomeIcon },
}
</script>

<style>
.dropdown {
  display: inline-block;
  margin: 0 10px;
}
.submenu {
  display: flex;
  flex-direction: column;
  position: absolute;
  background-color: white;
  text-align: left;
  border-top: 2px solid var(--primary-color);
  padding: 10px;
  margin-top: 5px;
  transform-origin: top;
  transition: transform .4s ease-in-out;
  overflow: hidden;
}
.nav-link {
  cursor: pointer;
  color: var(--primary-color);
  margin: 0;
  padding: 0;
}

.nav-link.selected {
  color: var(--accent-color);
}

.slide-enter-from, .slide-leave-to{
  transform: scaleY(0);
}
</style>