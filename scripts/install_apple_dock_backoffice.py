import os

filepath = os.path.join('templates', 'backoffice', 'base.html')
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

is_crlf = '\r\n' in content
content_lf = content.replace('\r\n', '\n')

# 1. Replace the entire mobile header (removing the top horizontal pill bar and leaving clean top header + drawer)
old_mobile_header_start = """        <!-- MOBILE TOPBAR & DRAWER ULTRA-PRO (STYLE LINEAR & APPLE) -->"""
old_mobile_header_end = """        </header>"""

start_pos = content_lf.find(old_mobile_header_start)
end_pos = content_lf.find(old_mobile_header_end, start_pos) + len(old_mobile_header_end)

assert start_pos != -1 and end_pos != -1, "Mobile header block not found in backoffice/base.html"

new_mobile_header = """        <!-- MOBILE TOPBAR ÉPURÉE STYLE APPLE (EN-TÊTE FIXE SANS ENCOMBREMENT) -->
        <header class="lg:hidden bg-[#0f172a]/95 backdrop-blur-xl text-white border-b border-slate-800 sticky top-0 z-40">
            <div class="px-4 h-12 flex items-center justify-between">
                <div class="flex items-center gap-2.5">
                    <a href="{% url 'backoffice:dashboard' %}" class="flex items-center gap-2 group">
                        <div class="w-7 h-7 rounded-lg bg-gradient-to-tr from-amber-500 to-yellow-400 flex items-center justify-center text-slate-950 font-black text-xs shadow-xs">
                            O
                        </div>
                        <div class="flex items-baseline gap-1.5">
                            <span class="font-heading font-black text-xs tracking-tight text-white">ONIZOUKA</span>
                            <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-amber-400/20 text-amber-300 border border-amber-400/30 font-bold">ERP</span>
                        </div>
                    </a>
                </div>

                <div class="flex items-center gap-2.5">
                    <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 text-[10px] font-bold border border-emerald-500/30">
                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                        <span>En direct</span>
                    </span>

                    <a href="{% url 'shop:home' %}" target="_blank" 
                       class="px-2.5 py-1 text-[11px] font-bold rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 transition shadow-xs flex items-center gap-1">
                        <span>Boutique</span>
                        <svg class="w-3 h-3 stroke-[2.2]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 6H5.25A2.25 2.25 0 003 8.25v10.5A2.25 2.25 0 005.25 21h10.5A2.25 2.25 0 0018 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
                        </svg>
                    </a>
                </div>
            </div>
            
            <!-- Mobile Drawer Menu Complet (Rétractable) -->
            <div x-show="mobileMenuOpen" 
                 x-cloak
                 x-transition:enter="transition ease-out duration-200"
                 x-transition:enter-start="opacity-0 -translate-y-3"
                 x-transition:enter-end="opacity-100 translate-y-0"
                 x-transition:leave="transition ease-in duration-150"
                 x-transition:leave-start="opacity-100 translate-y-0"
                 x-transition:leave-end="opacity-0 -translate-y-3"
                 @click.outside="mobileMenuOpen = false"
                 class="p-3.5 bg-[#0b1120] border-b border-slate-800 space-y-1 text-xs select-none shadow-2xl" 
                 style="display: none;">
                
                <div class="text-[10px] font-bold uppercase tracking-wider text-slate-500 px-2 pt-1 pb-1">
                    Modules de Gestion Direction
                </div>

                <a href="{% url 'backoffice:dashboard' %}" class="flex items-center gap-2.5 px-3 py-2 rounded-xl text-slate-200 hover:bg-slate-800 {% if current_page == 'dashboard' %}bg-slate-800 text-amber-400 font-bold border-l-2 border-amber-400{% endif %}">
                    <svg class="w-4 h-4 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z"/></svg>
                    <span>Tableau de bord exécutif</span>
                </a>

                <a href="{% url 'backoffice:orders' %}" class="flex items-center justify-between px-3 py-2 rounded-xl text-slate-200 hover:bg-slate-800 {% if current_page == 'orders' %}bg-slate-800 text-amber-400 font-bold border-l-2 border-amber-400{% endif %}">
                    <div class="flex items-center gap-2.5">
                        <svg class="w-4 h-4 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25c-.669 0-1.189-.578-1.119-1.243l1.263-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"/></svg>
                        <span>Commandes & Ventes</span>
                    </div>
                    {% if pending_orders_count and pending_orders_count > 0 %}
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-400 text-slate-950 font-mono">{{ pending_orders_count }}</span>
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
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-rose-500 text-white font-mono">{{ low_stock_count }}</span>
                    {% endif %}
                </a>

                <a href="{% url 'backoffice:clients' %}" class="flex items-center gap-2.5 px-3 py-2 rounded-xl text-slate-200 hover:bg-slate-800 {% if current_page == 'clients' %}bg-slate-800 text-amber-400 font-bold border-l-2 border-amber-400{% endif %}">
                    <svg class="w-4 h-4 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z"/></svg>
                    <span>Clients & Répertoire Bamako</span>
                </a>

                <a href="{% url 'backoffice:users' %}" class="flex items-center gap-2.5 px-3 py-2 rounded-xl text-slate-200 hover:bg-slate-800 {% if current_page == 'users' %}bg-slate-800 text-amber-400 font-bold border-l-2 border-amber-400{% endif %}">
                    <svg class="w-4 h-4 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.999-3.199a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z"/></svg>
                    <span>Équipe & Droits d'Accès</span>
                </a>

                <a href="{% url 'backoffice:settings' %}" class="flex items-center gap-2.5 px-3 py-2 rounded-xl text-slate-200 hover:bg-slate-800 {% if current_page == 'settings' %}bg-slate-800 text-amber-400 font-bold border-l-2 border-amber-400{% endif %}">
                    <svg class="w-4 h-4 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M10.343 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.325.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.004.827c-.292.24-.437.613-.43.992a7.723 7.723 0 010 .255c-.007.378.138.75.43.99l1.004.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.6 6.6 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.019-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a7.023 7.023 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                    <span>Paramètres & Société</span>
                </a>

                <div class="pt-2 border-t border-slate-800/80">
                    <div class="p-2.5 rounded-xl bg-slate-900/90 border border-slate-800 flex items-center justify-between">
                        <div class="flex items-center gap-2">
                            <div class="w-8 h-8 rounded-full bg-[#0f172a] text-amber-400 font-bold text-xs flex items-center justify-center border border-amber-400/40">
                                {{ request.user.username|slice:":1"|upper }}
                            </div>
                            <div>
                                <div class="font-bold text-slate-200 text-xs">{{ request.user.username }}</div>
                                <div class="text-[10px] text-amber-400 font-medium">{% if request.user.is_superuser %}Superadmin IT{% else %}Direction Bamako{% endif %}</div>
                            </div>
                        </div>
                        <a href="{% url 'account_logout' %}" class="px-2.5 py-1 rounded-lg bg-rose-500/10 text-rose-300 hover:bg-rose-500/20 border border-rose-500/30 text-[11px] font-bold transition">
                            Déconnexion
                        </a>
                    </div>
                </div>

            </div>
        </header>"""

content_lf = content_lf[:start_pos] + new_mobile_header + content_lf[end_pos:]

# 2. Add pb-24 to main content so content isn't covered by bottom dock
old_main = """        <!-- MAIN CONTENT AREA -->
        <main class="flex-1 flex flex-col min-w-0 bg-slate-50 min-h-screen">"""

new_main = """        <!-- MAIN CONTENT AREA (AVEC SAFE-PADDING POUR DOCK MOBILE) -->
        <main class="flex-1 flex flex-col min-w-0 bg-slate-50 min-h-screen pb-20 lg:pb-0">"""

content_lf = content_lf.replace(old_main, new_main, 1)

# 3. Add the authentic Apple Design Mobile Bottom Dock right before </body>
old_end = """    {% block extra_js %}{% endblock %}
</body>"""

new_end = """    <!-- ===== DOCK DE NAVIGATION MOBILE APPLE DESIGN HAUTE COUTURE (CALIBRE IOS ÉLITE) ===== -->
    <nav class="lg:hidden fixed bottom-0 left-0 right-0 z-50 bg-[#0f172a]/95 backdrop-blur-2xl border-t border-slate-800/90 shadow-[0_-8px_30px_rgba(0,0,0,0.4)] px-1 pt-1.5 pb-[max(env(safe-area-inset-bottom),8px)] select-none">
        <div class="flex items-center justify-around max-w-lg mx-auto">
            
            <!-- 1. Dashboard -->
            <a href="{% url 'backoffice:dashboard' %}" 
               class="flex flex-col items-center justify-center flex-1 py-1 transition-transform duration-100 active:scale-88 relative {% if current_page == 'dashboard' %}text-amber-400{% else %}text-slate-400 hover:text-slate-200{% endif %}">
                <div class="relative flex items-center justify-center">
                    <svg class="w-5 h-5 {% if current_page == 'dashboard' %}stroke-[2.2]{% else %}stroke-[1.8]{% endif %}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z" />
                    </svg>
                    {% if current_page == 'dashboard' %}
                    <span class="w-1 h-1 rounded-full bg-amber-400 absolute -bottom-1"></span>
                    {% endif %}
                </div>
                <span class="text-[10px] tracking-tight leading-none mt-1 {% if current_page == 'dashboard' %}font-extrabold text-amber-400{% else %}font-medium text-slate-400{% endif %}">
                    Dashboard
                </span>
            </a>

            <!-- 2. Commandes -->
            <a href="{% url 'backoffice:orders' %}" 
               class="flex flex-col items-center justify-center flex-1 py-1 transition-transform duration-100 active:scale-88 relative {% if current_page == 'orders' %}text-amber-400{% else %}text-slate-400 hover:text-slate-200{% endif %}">
                <div class="relative flex items-center justify-center">
                    <svg class="w-5 h-5 {% if current_page == 'orders' %}stroke-[2.2]{% else %}stroke-[1.8]{% endif %}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25c-.669 0-1.189-.578-1.119-1.243l1.263-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
                    </svg>
                    {% if pending_orders_count and pending_orders_count > 0 %}
                    <span class="absolute -top-1.5 -right-2 min-w-[16px] h-4 px-1 rounded-full bg-amber-400 text-slate-950 font-black text-[9px] flex items-center justify-center shadow-xs">
                        {{ pending_orders_count }}
                    </span>
                    {% endif %}
                    {% if current_page == 'orders' %}
                    <span class="w-1 h-1 rounded-full bg-amber-400 absolute -bottom-1"></span>
                    {% endif %}
                </div>
                <span class="text-[10px] tracking-tight leading-none mt-1 {% if current_page == 'orders' %}font-extrabold text-amber-400{% else %}font-medium text-slate-400{% endif %}">
                    Commandes
                </span>
            </a>

            <!-- 3. Catalogue -->
            <a href="{% url 'backoffice:products' %}" 
               class="flex flex-col items-center justify-center flex-1 py-1 transition-transform duration-100 active:scale-88 relative {% if current_page == 'products' %}text-amber-400{% else %}text-slate-400 hover:text-slate-200{% endif %}">
                <div class="relative flex items-center justify-center">
                    <svg class="w-5 h-5 {% if current_page == 'products' %}stroke-[2.2]{% else %}stroke-[1.8]{% endif %}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z" />
                    </svg>
                    {% if current_page == 'products' %}
                    <span class="w-1 h-1 rounded-full bg-amber-400 absolute -bottom-1"></span>
                    {% endif %}
                </div>
                <span class="text-[10px] tracking-tight leading-none mt-1 {% if current_page == 'products' %}font-extrabold text-amber-400{% else %}font-medium text-slate-400{% endif %}">
                    Catalogue
                </span>
            </a>

            <!-- 4. Stocks & Alertes -->
            <a href="{% url 'backoffice:stocks' %}" 
               class="flex flex-col items-center justify-center flex-1 py-1 transition-transform duration-100 active:scale-88 relative {% if current_page == 'stocks' %}text-amber-400{% else %}text-slate-400 hover:text-slate-200{% endif %}">
                <div class="relative flex items-center justify-center">
                    <svg class="w-5 h-5 {% if current_page == 'stocks' %}stroke-[2.2]{% else %}stroke-[1.8]{% endif %}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 12h16.5m-16.5 3.75h16.5M3.75 19.5h16.5M5.625 4.5h12.75a1.875 1.875 0 010 3.75H5.625a1.875 1.875 0 010-3.75z" />
                    </svg>
                    {% if low_stock_count and low_stock_count > 0 %}
                    <span class="absolute -top-1.5 -right-2 min-w-[16px] h-4 px-1 rounded-full bg-rose-500 text-white font-black text-[9px] flex items-center justify-center shadow-xs">
                        {{ low_stock_count }}
                    </span>
                    {% endif %}
                    {% if current_page == 'stocks' %}
                    <span class="w-1 h-1 rounded-full bg-amber-400 absolute -bottom-1"></span>
                    {% endif %}
                </div>
                <span class="text-[10px] tracking-tight leading-none mt-1 {% if current_page == 'stocks' %}font-extrabold text-amber-400{% else %}font-medium text-slate-400{% endif %}">
                    Stocks
                </span>
            </a>

            <!-- 5. Menu Plus (Ouvre le Drawer avec Clients, Équipe, Paramètres) -->
            <button type="button" 
                    @click="mobileMenuOpen = !mobileMenuOpen" 
                    class="flex flex-col items-center justify-center flex-1 py-1 transition-transform duration-100 active:scale-88 relative cursor-pointer"
                    :class="mobileMenuOpen ? 'text-amber-400' : 'text-slate-400 hover:text-slate-200'">
                <div class="relative flex items-center justify-center">
                    <svg class="w-5 h-5 stroke-[1.8]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                    </svg>
                    <span x-show="mobileMenuOpen" class="w-1 h-1 rounded-full bg-amber-400 absolute -bottom-1"></span>
                </div>
                <span class="text-[10px] tracking-tight leading-none mt-1 font-medium" :class="mobileMenuOpen ? 'font-extrabold text-amber-400' : 'text-slate-400'">
                    Menu
                </span>
            </button>

        </div>
    </nav>

    {% block extra_js %}{% endblock %}
</body>"""

assert old_end in content_lf, "old_end not found in backoffice/base.html"
content_lf = content_lf.replace(old_end, new_end, 1)

final_content = content_lf.replace('\n', '\r\n') if is_crlf else content_lf
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("backoffice/base.html successfully updated with authentic Apple Bottom Dock navigation!")
