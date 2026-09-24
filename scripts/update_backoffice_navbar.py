import os

filepath = os.path.join('templates', 'backoffice', 'base.html')
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

is_crlf = '\r\n' in content
content_lf = content.replace('\r\n', '\n')

old_mobile_header = """        <!-- MOBILE TOPBAR & DRAWER -->
        <header class="lg:hidden bg-[#0f172a] text-white border-b border-slate-800 sticky top-0 z-40">
            <div class="px-4 h-12 flex items-center justify-between">
                <div class="flex items-center gap-2.5">
                    <button @click="mobileMenuOpen = !mobileMenuOpen" 
                            type="button" 
                            class="p-1.5 -ml-1.5 rounded text-slate-300 hover:text-white hover:bg-slate-800 focus:outline-none transition"
                            aria-label="Ouvrir le menu">
                        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                    </button>
                    <a href="{% url 'backoffice:dashboard' %}" class="flex items-center gap-2">
                        <div class="w-6 h-6 rounded bg-amber-500 flex items-center justify-center text-slate-950 font-black text-xs">O</div>
                        <span class="font-heading font-bold text-xs tracking-tight text-white">ONIZOUKA ERP</span>
                    </a>
                </div>
                <div class="flex items-center gap-2">
                    <a href="{% url 'shop:home' %}" target="_blank" class="px-2.5 py-1 text-[11px] font-medium rounded bg-slate-800 text-slate-200 border border-slate-700">
                        Boutique ↗
                    </a>
                </div>
            </div>
            
            <!-- Mobile Drawer Menu -->
            <div x-show="mobileMenuOpen" 
                 x-transition:enter="transition ease-out duration-150"
                 x-transition:enter-start="opacity-0 -translate-y-2"
                 x-transition:enter-end="opacity-100 translate-y-0"
                 x-transition:leave="transition ease-in duration-100"
                 x-transition:leave-start="opacity-100 translate-y-0"
                 x-transition:leave-end="opacity-0 -translate-y-2"
                 class="p-3 bg-[#0b1120] border-b border-slate-800 space-y-1 text-xs" 
                 style="display: none;">
                <a href="{% url 'backoffice:dashboard' %}" class="block px-3 py-2 rounded text-slate-200 hover:bg-slate-800">Tableau de bord</a>
                <a href="{% url 'backoffice:orders' %}" class="block px-3 py-2 rounded text-slate-200 hover:bg-slate-800">Commandes</a>
                <a href="{% url 'backoffice:products' %}" class="block px-3 py-2 rounded text-slate-200 hover:bg-slate-800">Catalogue & Prix</a>
                <a href="{% url 'backoffice:stocks' %}" class="block px-3 py-2 rounded text-slate-200 hover:bg-slate-800">Stocks & Alertes</a>
                <a href="{% url 'backoffice:clients' %}" class="block px-3 py-2 rounded text-slate-200 hover:bg-slate-800">Clients</a>
                <a href="{% url 'backoffice:users' %}" class="block px-3 py-2 rounded text-slate-200 hover:bg-slate-800">Équipe & Accès</a>
                <a href="{% url 'backoffice:settings' %}" class="block px-3 py-2 rounded text-slate-200 hover:bg-slate-800">Paramètres & Société</a>
                <a href="{% url 'account_logout' %}" class="block px-3 py-2 rounded text-rose-300 hover:bg-rose-950/30">Déconnexion</a>
            </div>
        </header>"""

new_mobile_header = """        <!-- MOBILE TOPBAR & DRAWER ULTRA-PRO (STYLE LINEAR & APPLE) -->
        <header class="lg:hidden bg-[#0f172a] text-white border-b border-slate-800 sticky top-0 z-40">
            <div class="px-3.5 h-12 flex items-center justify-between">
                <div class="flex items-center gap-2">
                    <button @click="mobileMenuOpen = !mobileMenuOpen" 
                            type="button" 
                            class="p-1.5 -ml-1 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800 focus:outline-none transition active:scale-95"
                            aria-label="Ouvrir le menu">
                        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                    </button>
                    <a href="{% url 'backoffice:dashboard' %}" class="flex items-center gap-2">
                        <div class="w-6 h-6 rounded bg-gradient-to-tr from-amber-500 to-yellow-400 flex items-center justify-center text-slate-950 font-black text-xs shadow-xs">O</div>
                        <div class="flex items-center gap-1.5">
                            <span class="font-heading font-bold text-xs tracking-tight text-white">ONIZOUKA</span>
                            <span class="text-[9px] font-mono px-1 py-0.2 rounded bg-amber-400/20 text-amber-300 border border-amber-400/30">ERP</span>
                        </div>
                    </a>
                </div>
                <div class="flex items-center gap-2">
                    <span class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 text-[10px] font-bold border border-emerald-500/30">
                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                        <span class="hidden sm:inline">En direct</span>
                    </span>
                    <a href="{% url 'shop:home' %}" target="_blank" class="px-2.5 py-1 text-[11px] font-bold rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 transition shadow-xs flex items-center gap-1">
                        <span>Boutique</span>
                        <span class="text-[10px]">&rarr;</span>
                    </a>
                </div>
            </div>

            <!-- CARROUSEL HORIZONTAL DES ONGLETS DE GESTION RAPIDE SUR MOBILE -->
            <div class="px-3 py-1.5 bg-[#0b1120] border-t border-slate-800/80 overflow-x-auto no-scrollbar flex items-center gap-1.5 select-none text-[11px]">
                <a href="{% url 'backoffice:dashboard' %}" 
                   class="px-2.5 py-1 rounded-full whitespace-nowrap shrink-0 transition-all font-bold {% if current_page == 'dashboard' %}bg-amber-500 text-slate-950 shadow-xs{% else %}text-slate-300 hover:text-white bg-slate-800/70{% endif %}">
                    Dashboard
                </a>
                <a href="{% url 'backoffice:orders' %}" 
                   class="px-2.5 py-1 rounded-full whitespace-nowrap shrink-0 transition-all font-bold flex items-center gap-1 {% if current_page == 'orders' %}bg-amber-500 text-slate-950 shadow-xs{% else %}text-slate-300 hover:text-white bg-slate-800/70{% endif %}">
                    <span>Commandes</span>
                    {% if pending_orders_count and pending_orders_count > 0 %}
                    <span class="text-[9px] px-1 rounded-full bg-amber-400 text-slate-950 font-black">{{ pending_orders_count }}</span>
                    {% endif %}
                </a>
                <a href="{% url 'backoffice:products' %}" 
                   class="px-2.5 py-1 rounded-full whitespace-nowrap shrink-0 transition-all font-bold {% if current_page == 'products' %}bg-amber-500 text-slate-950 shadow-xs{% else %}text-slate-300 hover:text-white bg-slate-800/70{% endif %}">
                    Catalogue
                </a>
                <a href="{% url 'backoffice:stocks' %}" 
                   class="px-2.5 py-1 rounded-full whitespace-nowrap shrink-0 transition-all font-bold flex items-center gap-1 {% if current_page == 'stocks' %}bg-amber-500 text-slate-950 shadow-xs{% else %}text-slate-300 hover:text-white bg-slate-800/70{% endif %}">
                    <span>Stocks</span>
                    {% if low_stock_count and low_stock_count > 0 %}
                    <span class="text-[9px] px-1 rounded-full bg-rose-500 text-white font-black">{{ low_stock_count }}</span>
                    {% endif %}
                </a>
                <a href="{% url 'backoffice:clients' %}" 
                   class="px-2.5 py-1 rounded-full whitespace-nowrap shrink-0 transition-all font-bold {% if current_page == 'clients' %}bg-amber-500 text-slate-950 shadow-xs{% else %}text-slate-300 hover:text-white bg-slate-800/70{% endif %}">
                    Clients
                </a>
                <a href="{% url 'backoffice:settings' %}" 
                   class="px-2.5 py-1 rounded-full whitespace-nowrap shrink-0 transition-all font-bold {% if current_page == 'settings' %}bg-amber-500 text-slate-950 shadow-xs{% else %}text-slate-300 hover:text-white bg-slate-800/70{% endif %}">
                    Société
                </a>
            </div>
            
            <!-- Mobile Drawer Menu Complet avec Icônes & Cartes -->
            <div x-show="mobileMenuOpen" 
                 x-transition:enter="transition ease-out duration-200"
                 x-transition:enter-start="opacity-0 -translate-y-2"
                 x-transition:enter-end="opacity-100 translate-y-0"
                 x-transition:leave="transition ease-in duration-150"
                 x-transition:leave-start="opacity-100 translate-y-0"
                 x-transition:leave-end="opacity-0 -translate-y-2"
                 class="p-3 bg-[#0b1120] border-b border-slate-800 space-y-1 text-xs select-none" 
                 style="display: none;">
                
                <div class="text-[10px] font-bold uppercase tracking-wider text-slate-500 px-2 pt-1 pb-1">
                    Gestion Commerciale Direction
                </div>

                <a href="{% url 'backoffice:dashboard' %}" class="flex items-center gap-2.5 px-3 py-2 rounded-xl text-slate-200 hover:bg-slate-800 {% if current_page == 'dashboard' %}bg-slate-800 text-amber-400 font-bold border-l-2 border-amber-400{% endif %}">
                    <svg class="w-4 h-4 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z"/></svg>
                    <span>Tableau de bord</span>
                </a>

                <a href="{% url 'backoffice:orders' %}" class="flex items-center justify-between px-3 py-2 rounded-xl text-slate-200 hover:bg-slate-800 {% if current_page == 'orders' %}bg-slate-800 text-amber-400 font-bold border-l-2 border-amber-400{% endif %}">
                    <div class="flex items-center gap-2.5">
                        <svg class="w-4 h-4 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25c-.669 0-1.189-.578-1.119-1.243l1.263-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"/></svg>
                        <span>Commandes</span>
                    </div>
                    {% if pending_orders_count and pending_orders_count > 0 %}
                    <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-amber-400/20 text-amber-300 font-mono">{{ pending_orders_count }}</span>
                    {% endif %}
                </a>

                <a href="{% url 'backoffice:products' %}" class="flex items-center gap-2.5 px-3 py-2 rounded-xl text-slate-200 hover:bg-slate-800 {% if current_page == 'products' %}bg-slate-800 text-amber-400 font-bold border-l-2 border-amber-400{% endif %}">
                    <svg class="w-4 h-4 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z"/></svg>
                    <span>Catalogue & Prix</span>
                </a>

                <a href="{% url 'backoffice:stocks' %}" class="flex items-center justify-between px-3 py-2 rounded-xl text-slate-200 hover:bg-slate-800 {% if current_page == 'stocks' %}bg-slate-800 text-amber-400 font-bold border-l-2 border-amber-400{% endif %}">
                    <div class="flex items-center gap-2.5">
                        <svg class="w-4 h-4 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M3.75 12h16.5m-16.5 3.75h16.5M3.75 19.5h16.5M5.625 4.5h12.75a1.875 1.875 0 010 3.75H5.625a1.875 1.875 0 010-3.75z"/></svg>
                        <span>Stocks & Alertes</span>
                    </div>
                    {% if low_stock_count and low_stock_count > 0 %}
                    <span class="text-[10px] font-bold px-1.5 py-0.2 rounded bg-rose-500/20 text-rose-300 font-mono">{{ low_stock_count }}</span>
                    {% endif %}
                </a>

                <a href="{% url 'backoffice:clients' %}" class="flex items-center gap-2.5 px-3 py-2 rounded-xl text-slate-200 hover:bg-slate-800 {% if current_page == 'clients' %}bg-slate-800 text-amber-400 font-bold border-l-2 border-amber-400{% endif %}">
                    <svg class="w-4 h-4 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z"/></svg>
                    <span>Clients & Bamako</span>
                </a>

                <a href="{% url 'backoffice:users' %}" class="flex items-center gap-2.5 px-3 py-2 rounded-xl text-slate-200 hover:bg-slate-800 {% if current_page == 'users' %}bg-slate-800 text-amber-400 font-bold border-l-2 border-amber-400{% endif %}">
                    <svg class="w-4 h-4 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.999-3.199a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z"/></svg>
                    <span>Équipe & Accès</span>
                </a>

                <a href="{% url 'backoffice:settings' %}" class="flex items-center gap-2.5 px-3 py-2 rounded-xl text-slate-200 hover:bg-slate-800 {% if current_page == 'settings' %}bg-slate-800 text-amber-400 font-bold border-l-2 border-amber-400{% endif %}">
                    <svg class="w-4 h-4 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M10.343 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.325.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.004.827c-.292.24-.437.613-.43.992a7.723 7.723 0 010 .255c-.007.378.138.75.43.99l1.004.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.6 6.6 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.019-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a7.023 7.023 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                    <span>Paramètres & Société</span>
                </a>

                <div class="pt-2 border-t border-slate-800/80">
                    <div class="p-2 rounded-xl bg-slate-900/90 border border-slate-800 flex items-center justify-between">
                        <div class="flex items-center gap-2">
                            <div class="w-7 h-7 rounded-full bg-amber-500 text-slate-950 font-bold text-xs flex items-center justify-center">
                                {{ request.user.username|slice:":1"|upper }}
                            </div>
                            <div>
                                <div class="font-bold text-slate-200 text-xs">{{ request.user.username }}</div>
                                <div class="text-[10px] text-amber-400">Direction Bamako</div>
                            </div>
                        </div>
                        <a href="{% url 'account_logout' %}" class="px-2.5 py-1 rounded-lg bg-rose-500/10 text-rose-300 border border-rose-500/20 text-[11px] font-bold">
                            Déconnexion
                        </a>
                    </div>
                </div>

            </div>
        </header>"""

assert old_mobile_header in content_lf, "old_mobile_header not found in backoffice/base.html"
content_lf = content_lf.replace(old_mobile_header, new_mobile_header, 1)

old_desktop_topbar = """            <!-- TOPBAR DESKTOP MINIMALISTE HAUTE DENSITÉ (H-11 = 44px) -->
            <div class="hidden lg:flex items-center justify-between px-6 h-11 bg-white border-b border-slate-200 sticky top-0 z-20">
                <div class="flex items-center gap-3 text-xs text-slate-500">
                    <span class="inline-flex items-center gap-1.5 text-slate-700 font-medium">
                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                        Système en direct
                    </span>
                    <span class="text-slate-300">|</span>
                    <span>Bamako, Mali (GMT)</span>
                    <span class="text-slate-300">|</span>
                    <span>Monnaie : <strong class="text-slate-700 font-medium">FCFA (XOF)</strong></span>
                </div>
                <div class="flex items-center gap-3 text-xs">
                    <a href="{% url 'shop:home' %}" target="_blank" class="inline-flex items-center gap-1 px-2.5 py-1 rounded text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition font-medium">
                        <span>Voir la boutique</span>
                        <span class="text-[10px]">↗</span>
                    </a>
                    <span class="text-slate-300">|</span>
                    <div class="flex items-center gap-1.5 text-slate-600">
                        <span class="text-slate-400">Opérateur :</span>
                        <span class="font-medium text-slate-800 font-mono text-[11px]">{{ request.user.username }}</span>
                    </div>
                </div>
            </div>"""

new_desktop_topbar = """            <!-- TOPBAR DESKTOP EXECUTIVE HAUTE PRÉCISION (STYLE LINEAR & APPLE) -->
            <div class="hidden lg:flex items-center justify-between px-6 h-13 bg-white/95 backdrop-blur-md border-b border-slate-200/90 sticky top-0 z-20 shadow-xs">
                
                <!-- Fil d'Ariane & Statut Direction -->
                <div class="flex items-center gap-3 text-xs">
                    <div class="flex items-center gap-2">
                        <span class="font-heading font-black text-xs text-slate-900 tracking-tight flex items-center gap-1.5">
                            <span class="w-2 h-2 rounded-full bg-amber-500"></span>
                            Direction ERP
                        </span>
                        <span class="text-slate-300">/</span>
                        <span class="font-bold text-slate-700 uppercase tracking-wider text-[11px] font-mono">
                            {{ current_page|default:'Tableau de bord'|title }}
                        </span>
                    </div>

                    <span class="text-slate-200">|</span>

                    <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 text-[10px] font-bold border border-emerald-200/60">
                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                        <span>Système en direct</span>
                    </span>

                    <span class="text-slate-200">|</span>
                    <span class="text-slate-400 text-[11px]">Grand Marché (Dabanani, Bamako)</span>
                    <span class="text-slate-200">|</span>
                    <span class="font-mono text-[11px] text-amber-700 font-semibold bg-amber-50 px-2 py-0.5 rounded-md border border-amber-200/60">FCFA (XOF)</span>
                </div>

                <!-- Actions Rapides & Profil Direction -->
                <div class="flex items-center gap-3 text-xs">
                    
                    <!-- Bouton Nouveau Produit Shortcut -->
                    <a href="{% url 'backoffice:product_create' %}" 
                       class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-black text-white font-bold text-xs shadow-xs transition active:scale-95 border border-slate-800">
                        <svg class="w-3.5 h-3.5 text-amber-400 stroke-[2.5]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                        </svg>
                        <span>Ajouter un produit</span>
                    </a>

                    <!-- Bouton Voir la Boutique Flambant Neuf -->
                    <a href="{% url 'shop:home' %}" target="_blank" 
                       class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-50 hover:bg-amber-100 text-amber-900 font-bold text-xs border border-amber-200/80 transition shadow-2xs">
                        <span>Voir la boutique</span>
                        <svg class="w-3 h-3 text-amber-700 stroke-[2.2]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 6H5.25A2.25 2.25 0 003 8.25v10.5A2.25 2.25 0 005.25 21h10.5A2.25 2.25 0 0018 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
                        </svg>
                    </a>

                    <span class="text-slate-200">|</span>

                    <!-- Profil Opérateur Compact -->
                    <div class="flex items-center gap-2 pl-1">
                        <div class="w-7 h-7 rounded-full bg-[#0f172a] text-amber-400 font-bold text-xs flex items-center justify-center shadow-xs border border-slate-700">
                            {{ request.user.username|slice:":1"|upper }}
                        </div>
                        <div class="text-left leading-tight hidden xl:block">
                            <span class="block text-xs font-bold text-slate-900 font-mono">{{ request.user.username }}</span>
                            <span class="block text-[10px] text-amber-600 font-bold">{% if request.user.is_superuser %}Superadmin IT{% else %}Direction{% endif %}</span>
                        </div>
                    </div>

                </div>

            </div>"""

assert old_desktop_topbar in content_lf, "old_desktop_topbar not found in backoffice/base.html"
content_lf = content_lf.replace(old_desktop_topbar, new_desktop_topbar, 1)

final_content = content_lf.replace('\n', '\r\n') if is_crlf else content_lf
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("templates/backoffice/base.html updated successfully with executive navbar and mobile carousel!")
