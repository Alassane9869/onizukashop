import os

filepath = os.path.join('templates', 'base.html')
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Normalize line endings
is_crlf = '\r\n' in content
content_lf = content.replace('\r\n', '\n')

# 1. Add x-cloak style in head if not present
if '[x-cloak]' not in content_lf:
    head_anchor = "{% block extra_head %}{% endblock %}"
    new_head = """  <style>
    [x-cloak] { display: none !important; }
  </style>
  {% block extra_head %}{% endblock %}"""
    content_lf = content_lf.replace(head_anchor, new_head, 1)
    print("1. Added [x-cloak] style to head.")

# 2. Update Top micro-bar + Header + Yellow Navigation Bar (Desktop + Mobile)
old_header_start = """  <!-- ===== BANDEAU SUPÉRIEUR JAUNE PREMIUM & OR (OFFICIEL BAMAKO) ===== -->"""
old_header_end = """  </header>"""

start_idx = content_lf.find(old_header_start)
end_idx = content_lf.find(old_header_end, start_idx) + len(old_header_end)

assert start_idx != -1 and end_idx != -1, "Header block not found in base.html"

new_header_code = """  <!-- ===== BANDEAU SUPÉRIEUR DIRECTION & SHOWROOM (CHARTE GESTION CALIBRE MONDIAL) ===== -->
  <div class="bg-[#0b1120] text-slate-300 text-[11px] sm:text-xs py-1.5 px-3 sm:px-6 font-medium border-b border-slate-800 select-none">
    <div class="max-w-7xl mx-auto flex justify-between items-center">
      <div class="flex items-center gap-2 sm:gap-3 truncate">
        <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 text-[10px] font-bold border border-emerald-500/30 shrink-0">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>Système en direct</span>
        </span>
        <span class="truncate hidden md:inline text-slate-400 text-xs">
          Showroom Grand Marché (Dabanani, Bamako) &bull; Livraison express 24h &bull; Garantie constructeur 12 à 24 mois
        </span>
        <span class="truncate md:hidden text-slate-400 text-[11px]">
          Grand Marché (Dabanani) &bull; Livraison 24h Bamako
        </span>
      </div>
      <div class="flex items-center gap-3 sm:gap-4 shrink-0 text-xs">
        <span class="hidden sm:inline text-slate-400 text-[11px]">Bamako, Mali (GMT)</span>
        <span class="hidden sm:inline text-slate-700">&bull;</span>
        <span class="hidden sm:inline text-amber-400 font-mono text-[11px] font-semibold">Monnaie : FCFA (XOF)</span>
        <span class="hidden sm:inline text-slate-700">&bull;</span>
        <a href="https://wa.me/{{ shop_settings.whatsapp_raw|default:'22392673799' }}" target="_blank" rel="noopener" class="text-white hover:text-amber-400 transition font-bold flex items-center gap-1.5">
          <svg class="w-3.5 h-3.5 fill-emerald-400" viewBox="0 0 24 24">
            <path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766 0-3.18-2.588-5.771-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.299.045-.677.063-1.092-.069-.252-.08-.575-.187-.988-.365-1.739-.751-2.874-2.502-2.961-2.617-.087-.116-.708-.94-.708-1.793s.448-1.273.607-1.446c.159-.173.346-.217.462-.217l.332.006c.106.005.249-.04.39.299.144.347.491 1.2.534 1.287.043.087.072.188.014.303-.058.116-.087.188-.173.289l-.26.303c-.087.087-.179.182-.077.357.101.174.45 1.054 1.325 1.833.687.612 1.267.801 1.447.888.181.087.289.073.397-.051.108-.124.462-.538.585-.722.123-.184.246-.153.411-.092.166.061 1.052.496 1.233.587.181.091.303.136.347.212.043.076.043.439-.101.844z"/>
          </svg>
          <span class="font-mono text-emerald-400 font-extrabold">{{ shop_settings.phone_whatsapp|default:'+223 92 67 37 99' }}</span>
        </a>
      </div>
    </div>
  </div>

  <!-- ===== GRAND HEADER ULTRA-PREMIUM (DESIGN APPLE & OBSIDIAN CHARTE GESTION) ===== -->
  <header 
    x-data="{ megaMenu: false, userMenu: false, boutiqueHover: false }" 
    class="sticky top-0 z-40 shadow-sm transition-all duration-300"
  >
    <!-- 1. PARTIE HAUTE BLANCHE/GLASS APPLE (LOGO, RECHERCHE CENTRALE, ACTIONS) -->
    <div class="bg-white/95 backdrop-blur-xl border-b border-slate-200/70">
      <div class="max-w-7xl mx-auto px-3 sm:px-6">
        
        <div class="flex items-center justify-between h-16 sm:h-20 gap-3 sm:gap-4 lg:gap-8">
          
          <!-- Logo Principal Grande Envergure -->
          <a href="{% url 'shop:home' %}" class="flex items-center gap-2.5 group select-none shrink-0" aria-label="Onizouka Shop Accueil">
            <div class="w-10 h-10 sm:w-11 sm:h-11 rounded-xl bg-gradient-to-tr from-amber-500 to-yellow-400 text-slate-950 flex items-center justify-center shrink-0 shadow-md shadow-amber-500/20 group-hover:scale-105 transition-transform duration-200">
              <svg class="w-6 h-6 fill-slate-950" viewBox="0 0 24 24">
                <path d="M19 6h-2c0-2.76-2.24-5-5-5S7 3.24 7 6H5c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-7-3c1.66 0 3 1.34 3 3H9c0-1.66 1.34-3 3-3zm7 17H5V8h14v12z"/>
              </svg>
            </div>
            <div class="flex flex-col">
              <div class="flex items-baseline">
                <span class="font-heading text-xl sm:text-2xl font-black tracking-tight text-slate-950">ONIZOUKA</span>
                <span class="text-amber-500 font-heading text-xl sm:text-2xl font-black ml-0.5">SHOP</span>
              </div>
              <span class="text-[10px] font-semibold text-slate-500 uppercase tracking-widest hidden sm:block -mt-1">
                Électroménager &bull; Froid &bull; Grand Marché Bamako
              </span>
            </div>
          </a>

          <!-- GRANDE BARRE DE RECHERCHE CENTRALE POUR PC (STYLE DARTY / APPLE STORE) -->
          <div class="hidden lg:flex flex-1 max-w-2xl mx-auto">
            <form action="{% url 'shop:search' %}" method="GET" class="relative w-full flex items-center">
              <div class="relative w-full flex items-center">
                <input 
                  type="text" 
                  name="q"
                  value="{{ request.GET.q|default:'' }}"
                  placeholder="Rechercher une marque, un modèle (ex: Samsung 55', Climatiseur Inverter...)" 
                  class="w-full h-11 pl-11 pr-32 rounded-full bg-slate-100 hover:bg-slate-100/90 focus:bg-white border border-slate-300/80 focus:border-amber-500 focus:ring-4 focus:ring-amber-500/10 text-xs sm:text-sm font-medium text-slate-900 placeholder:text-slate-500 transition-all outline-none"
                >
                <div class="absolute left-3.5 text-slate-400 pointer-events-none">
                  <svg class="w-5 h-5 stroke-[2]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
                  </svg>
                </div>
                <button 
                  type="submit" 
                  class="absolute right-1.5 h-8 px-4 rounded-full bg-slate-950 hover:bg-slate-900 active:scale-95 text-white text-xs font-bold transition shadow-xs flex items-center gap-1.5 border border-slate-800"
                >
                  <span class="text-amber-400 font-extrabold">Rechercher</span>
                  <svg class="w-3.5 h-3.5 stroke-[2.5] text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3"/>
                  </svg>
                </button>
              </div>
            </form>
          </div>

          <!-- BLOC ACTIONS DROITE (CONTACT BOUTIQUE + COMPTE + PANIER DÉTAILLÉ) -->
          <div class="flex items-center gap-1.5 sm:gap-3.5 shrink-0">
            
            <!-- Bouton Recherche Mobile Uniquement -->
            <button 
              type="button"
              @click="searchModal = true; $nextTick(() => { document.getElementById('apple-search-input')?.focus() })"
              class="lg:hidden w-9 h-9 rounded-full flex items-center justify-center text-slate-700 hover:text-slate-900 hover:bg-slate-100 active:scale-95 transition"
              aria-label="Rechercher"
            >
              <svg class="w-5 h-5 stroke-[2]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
              </svg>
            </button>

            <!-- Contact Boutique Direct sur Desktop avec Popover Info -->
            <div class="relative hidden xl:block" @mouseenter="boutiqueHover = true" @mouseleave="boutiqueHover = false">
              <a 
                href="{% url 'shop:contact' %}" 
                class="flex items-center gap-2.5 px-3 py-1.5 rounded-xl hover:bg-slate-100 transition group text-left"
              >
                <div class="w-8 h-8 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center shrink-0 group-hover:bg-amber-500 group-hover:text-slate-950 transition">
                  <svg class="w-4 h-4 stroke-[2]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z"/>
                  </svg>
                </div>
                <div>
                  <span class="block text-[10px] font-bold text-slate-400 uppercase tracking-wider">Boutique Bamako</span>
                  <span class="block text-xs font-bold text-slate-900">Grand Marché (Dabanani)</span>
                </div>
              </a>

              <!-- Popover Boutique Info -->
              <div 
                x-show="boutiqueHover"
                x-transition:enter="transition ease-out duration-150"
                x-transition:enter-start="opacity-0 translate-y-1"
                x-transition:enter-end="opacity-100 translate-y-0"
                x-transition:leave="transition ease-in duration-100"
                x-transition:leave-start="opacity-100 translate-y-0"
                x-transition:leave-end="opacity-0 translate-y-1"
                class="absolute right-0 top-full mt-1.5 w-64 p-3.5 bg-white rounded-2xl shadow-xl border border-slate-200 z-50 text-left"
                style="display: none;"
              >
                <p class="text-xs font-bold text-slate-900 font-heading">Boutique Principale Bamako</p>
                <p class="text-[11px] text-slate-500 mt-0.5">Grand Marché de Bamako, Dabanani</p>
                <div class="mt-2 pt-2 border-t border-slate-100 flex items-center justify-between text-[11px]">
                  <span class="text-emerald-600 font-bold">Ouvert 7j/7</span>
                  <span class="text-slate-500">08h30 - 20h30</span>
                </div>
                <a href="https://wa.me/{{ shop_settings.whatsapp_raw|default:'22392673799' }}" target="_blank" rel="noopener" class="mt-2.5 block text-center py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-[11px] transition shadow-xs">
                  Contacter sur WhatsApp
                </a>
              </div>
            </div>

            <!-- Compte Utilisateur Desktop avec Menu Déroulant Pro -->
            <div class="relative hidden sm:block" @mouseenter="userMenu = true" @mouseleave="userMenu = false">
              {% if user.is_authenticated %}
              <button 
                type="button"
                @click="userMenu = !userMenu"
                class="flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-bold text-slate-800 hover:text-amber-600 hover:bg-slate-100 transition"
              >
                <div class="w-8 h-8 rounded-full bg-[#0f172a] text-amber-400 flex items-center justify-center font-bold text-xs shadow-xs">
                  {{ user.first_name|default:user.username|slice:":1"|upper }}
                </div>
                <div class="text-left hidden lg:block">
                  <span class="block text-[10px] text-slate-400 font-medium">Mon compte</span>
                  <span class="block text-xs font-bold text-slate-900 truncate max-w-[95px]">{{ user.first_name|default:user.username }}</span>
                </div>
                <svg class="w-3.5 h-3.5 text-slate-400 transition-transform hidden lg:block" :class="userMenu ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.5 8.25l-7.5 7.5-7.5-7.5"/>
                </svg>
              </button>
              {% else %}
              <button 
                type="button"
                @click="userMenu = !userMenu"
                class="flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-bold text-slate-800 hover:text-amber-600 hover:bg-slate-100 transition"
              >
                <div class="w-8 h-8 rounded-full bg-slate-100 text-slate-600 flex items-center justify-center">
                  <svg class="w-4 h-4 stroke-[2]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                  </svg>
                </div>
                <div class="text-left hidden lg:block">
                  <span class="block text-[10px] text-slate-400 font-medium">Espace Client</span>
                  <span class="block text-xs font-bold text-slate-900">Se connecter</span>
                </div>
                <svg class="w-3.5 h-3.5 text-slate-400 transition-transform hidden lg:block" :class="userMenu ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.5 8.25l-7.5 7.5-7.5-7.5"/>
                </svg>
              </button>
              {% endif %}

              <!-- Dropdown Menu Compte -->
              <div 
                x-show="userMenu"
                x-transition:enter="transition ease-out duration-150"
                x-transition:enter-start="opacity-0 translate-y-1"
                x-transition:enter-end="opacity-100 translate-y-0"
                x-transition:leave="transition ease-in duration-100"
                x-transition:leave-start="opacity-100 translate-y-0"
                x-transition:leave-end="opacity-0 translate-y-1"
                @click.away="userMenu = false"
                class="absolute right-0 top-full mt-1.5 w-56 p-2 bg-white rounded-2xl shadow-xl border border-slate-200 z-50 text-left"
                style="display: none;"
              >
                {% if user.is_authenticated %}
                <div class="px-3 py-2 border-b border-slate-100 mb-1">
                  <div class="flex items-center justify-between">
                    <p class="text-xs font-bold text-slate-900 truncate">{{ user.get_full_name|default:user.username }}</p>
                    {% if user.is_staff %}
                    <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-amber-400/20 text-amber-800 font-bold border border-amber-400/40">Direction</span>
                    {% endif %}
                  </div>
                  <p class="text-[10px] text-slate-500 truncate">{{ user.email }}</p>
                </div>

                {% if user.is_staff %}
                <!-- LIEN DIRECT VERS LE PORTAIL DE GESTION -->
                <a href="{% url 'backoffice:dashboard' %}" class="flex items-center justify-between gap-2 px-3 py-2.5 rounded-xl text-xs bg-[#0f172a] text-white hover:bg-black transition font-bold mb-2 shadow-xs border border-slate-800">
                  <div class="flex items-center gap-2">
                    <div class="w-4 h-4 rounded bg-amber-500 text-slate-950 font-bold text-[10px] flex items-center justify-center">O</div>
                    <span class="text-amber-300 font-bold">Portail Gestion</span>
                  </div>
                  <span class="text-[10px] bg-white/20 px-1.5 py-0.5 rounded text-white">Accès Pro →</span>
                </a>
                {% endif %}

                <a href="{% url 'accounts:dashboard' %}" class="flex items-center gap-2 px-3 py-2 rounded-lg text-xs text-slate-700 hover:bg-amber-50 hover:text-amber-700 transition font-medium">
                  <svg class="w-4 h-4 stroke-[1.8]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z"/></svg>
                  Tableau de bord client
                </a>
                <a href="{% url 'accounts:order_list' %}" class="flex items-center gap-2 px-3 py-2 rounded-lg text-xs text-slate-700 hover:bg-amber-50 hover:text-amber-700 transition font-medium">
                  <svg class="w-4 h-4 stroke-[1.8]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25c-.669 0-1.189-.578-1.119-1.243l1.263-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"/></svg>
                  Mes commandes
                </a>
                <a href="{% url 'accounts:profile_edit' %}" class="flex items-center gap-2 px-3 py-2 rounded-lg text-xs text-slate-700 hover:bg-amber-50 hover:text-amber-700 transition font-medium">
                  <svg class="w-4 h-4 stroke-[1.8]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L6.832 19.82a4.5 4.5 0 01-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 011.13-1.897L16.863 4.487zm0 0L19.5 7.125"/></svg>
                  Modifier mon profil
                </a>
                <div class="my-1 border-t border-slate-100"></div>
                <a href="{% url 'account_logout' %}" class="flex items-center gap-2 px-3 py-2 rounded-lg text-xs text-red-600 hover:bg-red-50 transition font-medium">
                  <svg class="w-4 h-4 stroke-[1.8]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9"/></svg>
                  Déconnexion
                </a>
                {% else %}
                <div class="p-2 space-y-2">
                  <a href="{% url 'account_login' %}" class="block text-center w-full py-2 rounded-xl bg-slate-950 hover:bg-black text-white font-bold text-xs transition shadow-xs">
                    Se connecter
                  </a>
                  <a href="{% url 'account_signup' %}" class="block text-center w-full py-1.5 rounded-xl border border-slate-200 hover:bg-slate-50 text-slate-800 font-bold text-xs transition">
                    Créer un compte
                  </a>
                  <div class="pt-2 border-t border-slate-100">
                    <a href="{% url 'orders:history' %}" class="block text-center text-[11px] text-slate-500 hover:text-amber-600 font-medium">
                      Suivi direct de commande &rarr;
                    </a>
                  </div>
                </div>
                {% endif %}
              </div>
            </div>

            <!-- Panier d'Achat Dynamique avec Badge et Label -->
            <a 
              href="{% url 'orders:cart' %}"
              class="flex items-center gap-2 px-3 py-2 rounded-xl bg-amber-50 hover:bg-amber-100/90 text-amber-700 transition group active:scale-95 border border-amber-200/60"
              aria-label="Mon Panier"
            >
              <div class="relative flex items-center justify-center">
                <svg class="w-5 h-5 stroke-[2] text-amber-600 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25c-.669 0-1.189-.578-1.119-1.243l1.263-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
                </svg>
                <span 
                  id="cart-badge"
                  class="cart-count-badge absolute -top-2 -right-2.5 min-w-[18px] h-[18px] px-1 bg-[#0f172a] text-amber-300 rounded-full text-[10px] font-black flex items-center justify-center shadow-xs border border-amber-400/30 {% if cart_count == 0 %}hidden{% endif %}"
                >
                  {{ cart_count|default:"0" }}
                </span>
              </div>
              <div class="hidden sm:block text-left">
                <span class="block text-[10px] text-amber-700 font-bold uppercase tracking-wider leading-none">Panier</span>
                <span class="block text-xs font-black text-slate-950 leading-tight">Commander</span>
              </div>
            </a>

          </div>

        </div>

        <!-- BARRE DE RECHERCHE RAPIDE MOBILE (STYLE AMAZON / APPLE MOBILE) -->
        <div class="lg:hidden pb-2.5 pt-0.5">
          <button 
            type="button" 
            @click="searchModal = true; $nextTick(() => { document.getElementById('apple-search-input')?.focus() })"
            class="w-full h-9.5 px-3.5 rounded-full bg-slate-100 hover:bg-slate-200/70 border border-slate-200/90 flex items-center justify-between text-xs text-slate-400 active:scale-[0.98] transition select-none shadow-2xs"
            aria-label="Rechercher un produit"
          >
            <span class="flex items-center gap-2 truncate">
              <svg class="w-4 h-4 text-slate-400 stroke-[2.2] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"/>
              </svg>
              <span class="text-slate-500 font-medium truncate">Rechercher frigo, climatiseur, TV...</span>
            </span>
            <span class="text-[10px] font-bold text-slate-900 bg-amber-400 px-2 py-0.5 rounded-full shadow-2xs shrink-0">
              Explorer
            </span>
          </button>
        </div>

      </div>
    </div>

    <!-- 2. ===== LA SIGNATURE NAV BARRE JAUNE (CALIBRE APPLE & RESPONSIVE MOBILE) ===== -->
    <div class="bg-gradient-to-r from-amber-400 via-amber-400 to-yellow-400 border-b border-amber-500/40 text-slate-950 select-none shadow-xs">
      
      <!-- VERSION DESKTOP (LG+) -->
      <nav class="hidden lg:flex max-w-7xl mx-auto px-4 sm:px-6 py-2 items-center justify-between text-xs font-bold relative">
        
        <!-- Bloc Gauche : Bouton Tous les Rayons (Mega-Menu) -->
        <div class="flex items-center gap-2">
          
          <!-- Bouton Capsule Mega-Menu Haute Couture (Obsidian & Gold) -->
          <div class="relative" @mouseenter="megaMenu = true" @mouseleave="megaMenu = false">
            <button 
              type="button" 
              @click="megaMenu = !megaMenu"
              class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#0f172a] hover:bg-black active:scale-95 text-white transition-all select-none shadow-sm font-bold text-xs border border-slate-800 cursor-pointer"
            >
              <svg class="w-3.5 h-3.5 text-amber-400 stroke-[2.2]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <rect x="3" y="3" width="7" height="7" rx="1.5" />
                <rect x="14" y="3" width="7" height="7" rx="1.5" />
                <rect x="14" y="14" width="7" height="7" rx="1.5" />
                <rect x="3" y="14" width="7" height="7" rx="1.5" />
              </svg>
              <span>Tous les rayons</span>
              <svg class="w-3 h-3 text-slate-400 transition-transform duration-200" :class="megaMenu ? 'rotate-180 text-amber-400' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19.5 8.25l-7.5 7.5-7.5-7.5"/>
              </svg>
            </button>

            <!-- PANNEAU MEGA-MENU HAUT DE GAMME (4 COLONNES) -->
            <div 
              x-show="megaMenu"
              x-transition:enter="transition ease-out duration-200"
              x-transition:enter-start="opacity-0 translate-y-2 scale-98"
              x-transition:enter-end="opacity-100 translate-y-0 scale-100"
              x-transition:leave="transition ease-in duration-150"
              x-transition:leave-start="opacity-100 translate-y-0 scale-100"
              x-transition:leave-end="opacity-0 translate-y-2 scale-98"
              @click.away="megaMenu = false"
              class="absolute left-0 top-full mt-2 w-[860px] bg-white/98 backdrop-blur-md rounded-2xl shadow-2xl border border-slate-200/90 p-6 z-50 text-left grid grid-cols-4 gap-6"
              style="display: none;"
            >
              <!-- Colonne 1: Froid -->
              <div class="space-y-3">
                <div class="flex items-center gap-2 pb-2 border-b border-slate-100">
                  <span class="w-2 h-2 rounded-full bg-blue-500"></span>
                  <a href="{% url 'shop:category' 'refrigerateurs' %}" class="font-extrabold text-slate-900 hover:text-amber-600 text-xs">
                    Froid & Conservation
                  </a>
                </div>
                <ul class="space-y-1.5 text-[11px] font-medium text-slate-600">
                  <li><a href="{% url 'shop:category' 'refrigerateurs' %}" class="hover:text-amber-600 block py-0.5">Réfrigérateurs Combinés No Frost</a></li>
                  <li><a href="{% url 'shop:category' 'refrigerateurs' %}" class="hover:text-amber-600 block py-0.5">Américains French Door 4 Portes</a></li>
                  <li><a href="{% url 'shop:category' 'refrigerateurs' %}" class="hover:text-amber-600 block py-0.5">Congélateurs Coffres Tropicalisés</a></li>
                  <li><a href="{% url 'shop:category' 'refrigerateurs' %}" class="hover:text-amber-600 block py-0.5">Mini-Bars & Caves de Service</a></li>
                  <li class="pt-1"><a href="{% url 'shop:category' 'refrigerateurs' %}" class="text-amber-600 font-bold block">Explorer tout le Froid &rarr;</a></li>
                </ul>
              </div>

              <!-- Colonne 2: Climatisation -->
              <div class="space-y-3">
                <div class="flex items-center gap-2 pb-2 border-b border-slate-100">
                  <span class="w-2 h-2 rounded-full bg-cyan-500"></span>
                  <a href="{% url 'shop:category' 'climatisation' %}" class="font-extrabold text-slate-900 hover:text-amber-600 text-xs">
                    Climatisation Climat T3
                  </a>
                </div>
                <ul class="space-y-1.5 text-[11px] font-medium text-slate-600">
                  <li><a href="{% url 'shop:category' 'climatisation' %}" class="hover:text-amber-600 block py-0.5">Split Inverter 1.5 CV (Chambres)</a></li>
                  <li><a href="{% url 'shop:category' 'climatisation' %}" class="hover:text-amber-600 block py-0.5">Split Inverter 2 CV & 2.5 CV (Salons)</a></li>
                  <li><a href="{% url 'shop:category' 'climatisation' %}" class="hover:text-amber-600 block py-0.5">Armoires de Climatisation Pro</a></li>
                  <li><a href="{% url 'shop:category' 'climatisation' %}" class="hover:text-amber-600 block py-0.5">Ventilateurs Turbo Silencieux</a></li>
                  <li class="pt-1"><a href="{% url 'shop:category' 'climatisation' %}" class="text-amber-600 font-bold block">Voir tous les Climatiseurs &rarr;</a></li>
                </ul>
              </div>

              <!-- Colonne 3: TV, Son & Cuisson -->
              <div class="space-y-3">
                <div class="flex items-center gap-2 pb-2 border-b border-slate-100">
                  <span class="w-2 h-2 rounded-full bg-purple-500"></span>
                  <a href="{% url 'shop:category' 'televiseurs' %}" class="font-extrabold text-slate-900 hover:text-amber-600 text-xs">
                    Image, Son & Cuisson
                  </a>
                </div>
                <ul class="space-y-1.5 text-[11px] font-medium text-slate-600">
                  <li><a href="{% url 'shop:category' 'televiseurs' %}" class="hover:text-amber-600 block py-0.5">Smart TV 4K OLED, QLED & UHD</a></li>
                  <li><a href="{% url 'shop:category' 'televiseurs' %}" class="hover:text-amber-600 block py-0.5">Barres de Son & Home Cinéma</a></li>
                  <li><a href="{% url 'shop:category' 'cuisinieres' %}" class="hover:text-amber-600 block py-0.5">Cuisinières 5 Feux Inox 90x60</a></li>
                  <li><a href="{% url 'shop:category' 'cuisinieres' %}" class="hover:text-amber-600 block py-0.5">Fours & Micro-Ondes Miroir</a></li>
                  <li class="pt-1"><a href="{% url 'shop:category' 'cuisinieres' %}" class="text-amber-600 font-bold block">Rayon Cuisson Complet &rarr;</a></li>
                </ul>
              </div>

              <!-- Colonne 4: Marques Officielles & Reassurance -->
              <div class="p-3.5 rounded-xl bg-amber-50/70 border border-amber-200/60 space-y-3">
                <p class="text-[10px] font-bold text-amber-700 uppercase tracking-wider">Partenaires Certifiés</p>
                <div class="grid grid-cols-2 gap-2 text-xs font-bold text-slate-800">
                  <span class="px-2 py-1 rounded bg-white border border-slate-200 text-center">Samsung</span>
                  <span class="px-2 py-1 rounded bg-white border border-slate-200 text-center">LG</span>
                  <span class="px-2 py-1 rounded bg-white border border-slate-200 text-center">Midea</span>
                  <span class="px-2 py-1 rounded bg-white border border-slate-200 text-center">Hisense</span>
                  <span class="px-2 py-1 rounded bg-white border border-slate-200 text-center">Beko</span>
                  <span class="px-2 py-1 rounded bg-white border border-slate-200 text-center">Philips</span>
                </div>
                <div class="pt-2 border-t border-amber-200/60 text-[10px] text-slate-600 space-y-1">
                  <p class="flex items-center gap-1 font-semibold text-slate-900">
                    <svg class="w-3.5 h-3.5 text-emerald-600 stroke-[2.5]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5"/></svg>
                    Garantie 24 Mois Constructeur
                  </p>
                  <p class="flex items-center gap-1 font-semibold text-slate-900">
                    <svg class="w-3.5 h-3.5 text-emerald-600 stroke-[2.5]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5"/></svg>
                    Livraison & Installation Bamako
                  </p>
                </div>
                <a href="{% url 'shop:catalog' %}" class="block text-center py-1.5 rounded-lg bg-slate-950 hover:bg-slate-900 text-white font-bold text-[11px] transition">
                  Tout le Catalogue (100+)
                </a>
              </div>

            </div>
          </div>
        </div>

        <!-- Bloc Centre : Rayons Phares (Typographie Apple & Micro-Pills) -->
        <div class="flex items-center gap-1">
          <a 
            href="{% url 'shop:category' 'refrigerateurs' %}" 
            class="px-3.5 py-1.5 rounded-full text-xs font-bold whitespace-nowrap transition-all {% if request.resolver_match.kwargs.slug == 'refrigerateurs' %}bg-[#0f172a] text-white shadow-xs{% else %}text-slate-950 hover:bg-black/10 active:scale-95{% endif %}"
          >
            Réfrigérateurs
          </a>
          <a 
            href="{% url 'shop:category' 'climatisation' %}" 
            class="px-3.5 py-1.5 rounded-full text-xs font-bold whitespace-nowrap transition-all {% if request.resolver_match.kwargs.slug == 'climatisation' %}bg-[#0f172a] text-white shadow-xs{% else %}text-slate-950 hover:bg-black/10 active:scale-95{% endif %}"
          >
            Climatiseurs
          </a>
          <a 
            href="{% url 'shop:category' 'televiseurs' %}" 
            class="px-3.5 py-1.5 rounded-full text-xs font-bold whitespace-nowrap transition-all {% if request.resolver_match.kwargs.slug == 'televiseurs' %}bg-[#0f172a] text-white shadow-xs{% else %}text-slate-950 hover:bg-black/10 active:scale-95{% endif %}"
          >
            Smart TV
          </a>
          <a 
            href="{% url 'shop:category' 'cuisinieres' %}" 
            class="px-3.5 py-1.5 rounded-full text-xs font-bold whitespace-nowrap transition-all {% if request.resolver_match.kwargs.slug == 'cuisinieres' %}bg-[#0f172a] text-white shadow-xs{% else %}text-slate-950 hover:bg-black/10 active:scale-95{% endif %}"
          >
            Cuisinières
          </a>
          <a 
            href="{% url 'shop:category' 'petit-electromenager' %}" 
            class="px-3.5 py-1.5 rounded-full text-xs font-bold whitespace-nowrap transition-all {% if request.resolver_match.kwargs.slug == 'petit-electromenager' %}bg-[#0f172a] text-white shadow-xs{% else %}text-slate-950 hover:bg-black/10 active:scale-95{% endif %}"
          >
            Petit Électro
          </a>
        </div>

        <!-- Bloc Droite : Ventes Flash Animées & Boutique Dabanani -->
        <div class="flex items-center gap-2 shrink-0">
          <!-- Badge Ventes Flash Dynamique & Élégant (Noir & Or) -->
          <a 
            href="{% url 'shop:catalog' %}?en_promo=true" 
            class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#0f172a] hover:bg-black text-amber-300 font-extrabold text-xs shadow-xs hover:shadow-sm hover:scale-[1.02] active:scale-[0.98] transition-all border border-slate-800"
            title="Consulter les offres flash disponibles à Bamako"
          >
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-amber-400"></span>
            </span>
            <span class="tracking-tight">Ventes Flash</span>
          </a>

          <!-- Boutique Grand Marché -->
          <a 
            href="{% url 'shop:contact' %}" 
            class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-slate-950 hover:bg-black/10 transition-all font-bold text-xs whitespace-nowrap"
            title="Notre showroom au Grand Marché de Bamako (Dabanani)"
          >
            <svg class="w-3.5 h-3.5 text-slate-950 stroke-[2.2]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 21v-7.5a.75.75 0 01.75-.75h3a.75.75 0 01.75.75V21m-4.5 0H2.36m11.14 0H18m0 0h3.64m-1.39 0V9.349m-16.5 11.651V9.35m0 0a3.001 3.001 0 003.75-.614A2.993 2.993 0 009 9.35c.773 0 1.492-.294 2.036-.78M15 9.35c.544.486 1.263.78 2.036.78a2.993 2.993 0 002.214-.964 3.001 3.001 0 00.75.614M3 6.75h18l-1.5-3H4.5L3 6.75z" />
            </svg>
            <span>Showroom Dabanani</span>
          </a>
        </div>

      </nav>

      <!-- VERSION MOBILE ULTRA-RESPONSIVE (APPLE CAROUSEL HORIZONTAL FLUIDE) -->
      <div class="lg:hidden px-3 py-2 overflow-x-auto no-scrollbar flex items-center gap-2 select-none">
        
        <!-- Bouton Rayons Mobile Minimaliste -->
        <a 
          href="{% url 'shop:catalog' %}" 
          class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#0f172a] text-white text-xs font-bold shrink-0 shadow-xs border border-slate-800"
        >
          <svg class="w-3.5 h-3.5 text-amber-400" viewBox="0 0 24 24" fill="currentColor">
            <rect x="3" y="3" width="7" height="7" rx="1.5" />
            <rect x="14" y="3" width="7" height="7" rx="1.5" />
            <rect x="14" y="14" width="7" height="7" rx="1.5" />
            <rect x="3" y="14" width="7" height="7" rx="1.5" />
          </svg>
          <span>Rayons</span>
        </a>

        <!-- Capsule Ventes Flash Mobile -->
        <a 
          href="{% url 'shop:catalog' %}?en_promo=true" 
          class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#0f172a] text-amber-300 text-xs font-extrabold shrink-0 shadow-xs border border-slate-800"
        >
          <span class="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse"></span>
          <span>Flash</span>
        </a>

        <!-- Catégories Mobiles Horizontales -->
        <a 
          href="{% url 'shop:category' 'refrigerateurs' %}" 
          class="px-3 py-1.5 rounded-full text-xs font-bold whitespace-nowrap shrink-0 transition-all {% if request.resolver_match.kwargs.slug == 'refrigerateurs' %}bg-[#0f172a] text-white shadow-xs{% else %}text-slate-950 hover:bg-black/10 active:scale-95{% endif %}"
        >
          Réfrigérateurs
        </a>
        <a 
          href="{% url 'shop:category' 'climatisation' %}" 
          class="px-3 py-1.5 rounded-full text-xs font-bold whitespace-nowrap shrink-0 transition-all {% if request.resolver_match.kwargs.slug == 'climatisation' %}bg-[#0f172a] text-white shadow-xs{% else %}text-slate-950 hover:bg-black/10 active:scale-95{% endif %}"
        >
          Climatiseurs
        </a>
        <a 
          href="{% url 'shop:category' 'televiseurs' %}" 
          class="px-3 py-1.5 rounded-full text-xs font-bold whitespace-nowrap shrink-0 transition-all {% if request.resolver_match.kwargs.slug == 'televiseurs' %}bg-[#0f172a] text-white shadow-xs{% else %}text-slate-950 hover:bg-black/10 active:scale-95{% endif %}"
        >
          Smart TV
        </a>
        <a 
          href="{% url 'shop:category' 'cuisinieres' %}" 
          class="px-3 py-1.5 rounded-full text-xs font-bold whitespace-nowrap shrink-0 transition-all {% if request.resolver_match.kwargs.slug == 'cuisinieres' %}bg-[#0f172a] text-white shadow-xs{% else %}text-slate-950 hover:bg-black/10 active:scale-95{% endif %}"
        >
          Cuisinières
        </a>
        <a 
          href="{% url 'shop:category' 'petit-electromenager' %}" 
          class="px-3 py-1.5 rounded-full text-xs font-bold whitespace-nowrap shrink-0 transition-all {% if request.resolver_match.kwargs.slug == 'petit-electromenager' %}bg-[#0f172a] text-white shadow-xs{% else %}text-slate-950 hover:bg-black/10 active:scale-95{% endif %}"
        >
          Petit Électro
        </a>
        <a 
          href="{% url 'shop:contact' %}" 
          class="px-3 py-1.5 rounded-full text-xs font-bold whitespace-nowrap shrink-0 text-slate-950 hover:bg-black/10"
        >
          Dabanani Showroom
        </a>

      </div>

    </div>

  </header>"""

content_lf = content_lf[:start_idx] + new_header_code + content_lf[end_idx:]

final_content = content_lf.replace('\n', '\r\n') if is_crlf else content_lf
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("templates/base.html updated successfully with Apple Yellow Navbar and Mobile Responsive Carousel!")
