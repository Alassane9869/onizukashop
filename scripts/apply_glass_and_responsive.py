import os

# -------------------------------------------------------------
# 1. Update templates/backoffice/base.html to Light Frosted Glass
# -------------------------------------------------------------
base_path = os.path.join('templates', 'backoffice', 'base.html')
with open(base_path, 'r', encoding='utf-8') as f:
    base_content = f.read()

is_crlf = '\r\n' in base_content
content_lf = base_content.replace('\r\n', '\n')

# Replace Mobile Header & Drawer with Light Frosted Glass
old_mobile_header_start = """        <!-- MOBILE TOPBAR ÉPURÉE STYLE APPLE (EN-TÊTE FIXE SANS ENCOMBREMENT) -->"""
old_mobile_header_end = """        </header>"""

start_pos = content_lf.find(old_mobile_header_start)
end_pos = content_lf.find(old_mobile_header_end, start_pos) + len(old_mobile_header_end)
assert start_pos != -1 and end_pos != -1, "Mobile header not found in backoffice/base.html"

new_mobile_header = """        <!-- MOBILE TOPBAR EFFET GLACE APPLE (TRANSLUCIDE & LUMINEUSE) -->
        <header class="lg:hidden bg-white/85 backdrop-blur-2xl text-slate-900 border-b border-slate-200/80 sticky top-0 z-40 shadow-xs">
            <div class="px-4 h-13 flex items-center justify-between">
                <div class="flex items-center gap-2.5">
                    <a href="{% url 'backoffice:dashboard' %}" class="flex items-center gap-2 group">
                        <div class="w-7 h-7 rounded-xl bg-gradient-to-tr from-amber-500 to-yellow-400 flex items-center justify-center text-slate-950 font-black text-xs shadow-xs">
                            O
                        </div>
                        <div class="flex items-baseline gap-1.5">
                            <span class="font-heading font-black text-xs tracking-tight text-slate-950">ONIZOUKA</span>
                            <span class="text-[9px] font-mono px-1.5 py-0.5 rounded-full bg-amber-100 text-amber-900 border border-amber-300 font-extrabold">ERP</span>
                        </div>
                    </a>
                </div>

                <div class="flex items-center gap-2.5">
                    <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 text-[10px] font-bold border border-emerald-200/80">
                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                        <span>En direct</span>
                    </span>

                    <a href="{% url 'shop:home' %}" target="_blank" 
                       class="px-2.5 py-1 text-xs font-bold rounded-xl bg-amber-500 hover:bg-amber-600 active:scale-95 text-slate-950 transition shadow-xs flex items-center gap-1">
                        <span>Boutique</span>
                        <svg class="w-3.5 h-3.5 stroke-[2.2]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 6H5.25A2.25 2.25 0 003 8.25v10.5A2.25 2.25 0 005.25 21h10.5A2.25 2.25 0 0018 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
                        </svg>
                    </a>
                </div>
            </div>
            
            <!-- Mobile Drawer Menu Complet - Effet Glace Lumineux Apple -->
            <div x-show="mobileMenuOpen" 
                 x-cloak
                 x-transition:enter="transition ease-out duration-200"
                 x-transition:enter-start="opacity-0 -translate-y-3"
                 x-transition:enter-end="opacity-100 translate-y-0"
                 x-transition:leave="transition ease-in duration-150"
                 x-transition:leave-start="opacity-100 translate-y-0"
                 x-transition:leave-end="opacity-0 -translate-y-3"
                 @click.outside="mobileMenuOpen = false"
                 class="p-4 bg-white/95 backdrop-blur-2xl border-b border-slate-200/80 space-y-1 text-xs select-none shadow-2xl" 
                 style="display: none;">
                
                <div class="text-[10px] font-bold uppercase tracking-wider text-slate-400 px-2 pt-1 pb-1">
                    Modules de Gestion Direction
                </div>

                <a href="{% url 'backoffice:dashboard' %}" class="flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-slate-700 hover:bg-slate-100/80 {% if current_page == 'dashboard' %}bg-amber-50 text-amber-900 font-bold border-l-2 border-amber-500{% endif %}">
                    <svg class="w-4 h-4 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z"/></svg>
                    <span>Tableau de bord exécutif</span>
                </a>

                <a href="{% url 'backoffice:orders' %}" class="flex items-center justify-between px-3 py-2.5 rounded-xl text-slate-700 hover:bg-slate-100/80 {% if current_page == 'orders' %}bg-amber-50 text-amber-900 font-bold border-l-2 border-amber-500{% endif %}">
                    <div class="flex items-center gap-2.5">
                        <svg class="w-4 h-4 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25c-.669 0-1.189-.578-1.119-1.243l1.263-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"/></svg>
                        <span>Commandes & Ventes</span>
                    </div>
                    {% if pending_orders_count and pending_orders_count > 0 %}
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-500 text-slate-950 font-mono">{{ pending_orders_count }}</span>
                    {% endif %}
                </a>

                <a href="{% url 'backoffice:products' %}" class="flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-slate-700 hover:bg-slate-100/80 {% if current_page == 'products' %}bg-amber-50 text-amber-900 font-bold border-l-2 border-amber-500{% endif %}">
                    <svg class="w-4 h-4 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z"/></svg>
                    <span>Catalogue & Prix</span>
                </a>

                <a href="{% url 'backoffice:stocks' %}" class="flex items-center justify-between px-3 py-2.5 rounded-xl text-slate-700 hover:bg-slate-100/80 {% if current_page == 'stocks' %}bg-amber-50 text-amber-900 font-bold border-l-2 border-amber-500{% endif %}">
                    <div class="flex items-center gap-2.5">
                        <svg class="w-4 h-4 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M3.75 12h16.5m-16.5 3.75h16.5M3.75 19.5h16.5M5.625 4.5h12.75a1.875 1.875 0 010 3.75H5.625a1.875 1.875 0 010-3.75z"/></svg>
                        <span>Stocks & Alertes</span>
                    </div>
                    {% if low_stock_count and low_stock_count > 0 %}
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-rose-500 text-white font-mono">{{ low_stock_count }}</span>
                    {% endif %}
                </a>

                <a href="{% url 'backoffice:clients' %}" class="flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-slate-700 hover:bg-slate-100/80 {% if current_page == 'clients' %}bg-amber-50 text-amber-900 font-bold border-l-2 border-amber-500{% endif %}">
                    <svg class="w-4 h-4 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z"/></svg>
                    <span>Clients & Répertoire Bamako</span>
                </a>

                <a href="{% url 'backoffice:users' %}" class="flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-slate-700 hover:bg-slate-100/80 {% if current_page == 'users' %}bg-amber-50 text-amber-900 font-bold border-l-2 border-amber-500{% endif %}">
                    <svg class="w-4 h-4 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.999-3.199a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z"/></svg>
                    <span>Équipe & Droits d'Accès</span>
                </a>

                <a href="{% url 'backoffice:settings' %}" class="flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-slate-700 hover:bg-slate-100/80 {% if current_page == 'settings' %}bg-amber-50 text-amber-900 font-bold border-l-2 border-amber-500{% endif %}">
                    <svg class="w-4 h-4 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M10.343 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.325.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.004.827c-.292.24-.437.613-.43.992a7.723 7.723 0 010 .255c-.007.378.138.75.43.99l1.004.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.6 6.6 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.019-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a7.023 7.023 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                    <span>Paramètres & Société</span>
                </a>

                <div class="pt-3 border-t border-slate-200">
                    <div class="p-3 rounded-2xl bg-slate-50 border border-slate-200/80 flex items-center justify-between">
                        <div class="flex items-center gap-2.5">
                            <div class="w-8 h-8 rounded-full bg-slate-900 text-amber-400 font-bold text-xs flex items-center justify-center">
                                {{ request.user.username|slice:":1"|upper }}
                            </div>
                            <div>
                                <div class="font-bold text-slate-900 text-xs">{{ request.user.username }}</div>
                                <div class="text-[10px] text-amber-700 font-bold">{% if request.user.is_superuser %}Superadmin IT{% else %}Direction Bamako{% endif %}</div>
                            </div>
                        </div>
                        <a href="{% url 'account_logout' %}" class="px-3 py-1.5 rounded-xl bg-rose-50 text-rose-700 hover:bg-rose-100 border border-rose-200 text-xs font-bold transition">
                            Déconnexion
                        </a>
                    </div>
                </div>

            </div>
        </header>"""

content_lf = content_lf[:start_pos] + new_mobile_header + content_lf[end_pos:]

# Replace Bottom Dock with Light Frosted Glass Apple Dock
old_dock_start = """    <!-- ===== DOCK DE NAVIGATION MOBILE APPLE DESIGN HAUTE COUTURE (CALIBRE IOS ÉLITE) ===== -->"""
old_dock_end = """    </nav>"""

dock_start_pos = content_lf.find(old_dock_start)
dock_end_pos = content_lf.find(old_dock_end, dock_start_pos) + len(old_dock_end)
assert dock_start_pos != -1 and dock_end_pos != -1, "Dock block not found in backoffice/base.html"

new_light_dock = """    <!-- ===== DOCK DE NAVIGATION MOBILE EFFET GLACE APPLE (LUMINEUX, BLUR 28PX, NATIVE IOS) ===== -->
    <nav class="lg:hidden fixed bottom-0 left-0 right-0 z-50 bg-white/85 backdrop-blur-2xl border-t border-slate-200/80 shadow-[0_-8px_30px_rgba(0,0,0,0.06)] px-1 pt-2 pb-[max(env(safe-area-inset-bottom),10px)] select-none">
        <div class="flex items-center justify-around max-w-lg mx-auto">
            
            <!-- 1. Dashboard -->
            <a href="{% url 'backoffice:dashboard' %}" 
               class="flex flex-col items-center justify-center flex-1 py-1 transition-transform duration-100 active:scale-88 relative {% if current_page == 'dashboard' %}text-amber-600{% else %}text-slate-400 hover:text-slate-700{% endif %}">
                <div class="relative flex items-center justify-center">
                    <svg class="w-5 h-5 {% if current_page == 'dashboard' %}stroke-[2.2] text-amber-500{% else %}stroke-[1.8]{% endif %}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z" />
                    </svg>
                    {% if current_page == 'dashboard' %}
                    <span class="w-1.5 h-1.5 rounded-full bg-amber-500 absolute -bottom-1"></span>
                    {% endif %}
                </div>
                <span class="text-[10px] tracking-tight leading-none mt-1 {% if current_page == 'dashboard' %}font-black text-amber-600{% else %}font-medium text-slate-500{% endif %}">
                    Dashboard
                </span>
            </a>

            <!-- 2. Commandes -->
            <a href="{% url 'backoffice:orders' %}" 
               class="flex flex-col items-center justify-center flex-1 py-1 transition-transform duration-100 active:scale-88 relative {% if current_page == 'orders' %}text-amber-600{% else %}text-slate-400 hover:text-slate-700{% endif %}">
                <div class="relative flex items-center justify-center">
                    <svg class="w-5 h-5 {% if current_page == 'orders' %}stroke-[2.2] text-amber-500{% else %}stroke-[1.8]{% endif %}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25c-.669 0-1.189-.578-1.119-1.243l1.263-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007zM8.625 10.5a.375.375 0 11-.75 0 .375.375 0 01.75 0zm7.5 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
                    </svg>
                    {% if pending_orders_count and pending_orders_count > 0 %}
                    <span class="absolute -top-1.5 -right-2 min-w-[17px] h-[17px] px-1 bg-amber-500 text-slate-950 font-black text-[9px] flex items-center justify-center rounded-full shadow-xs">
                        {{ pending_orders_count }}
                    </span>
                    {% endif %}
                    {% if current_page == 'orders' %}
                    <span class="w-1.5 h-1.5 rounded-full bg-amber-500 absolute -bottom-1"></span>
                    {% endif %}
                </div>
                <span class="text-[10px] tracking-tight leading-none mt-1 {% if current_page == 'orders' %}font-black text-amber-600{% else %}font-medium text-slate-500{% endif %}">
                    Commandes
                </span>
            </a>

            <!-- 3. Catalogue -->
            <a href="{% url 'backoffice:products' %}" 
               class="flex flex-col items-center justify-center flex-1 py-1 transition-transform duration-100 active:scale-88 relative {% if current_page == 'products' %}text-amber-600{% else %}text-slate-400 hover:text-slate-700{% endif %}">
                <div class="relative flex items-center justify-center">
                    <svg class="w-5 h-5 {% if current_page == 'products' %}stroke-[2.2] text-amber-500{% else %}stroke-[1.8]{% endif %}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M20.25 7.5l-.625 10.632a2.25 2.25 0 01-2.247 2.118H6.622a2.25 2.25 0 01-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z" />
                    </svg>
                    {% if current_page == 'products' %}
                    <span class="w-1.5 h-1.5 rounded-full bg-amber-500 absolute -bottom-1"></span>
                    {% endif %}
                </div>
                <span class="text-[10px] tracking-tight leading-none mt-1 {% if current_page == 'products' %}font-black text-amber-600{% else %}font-medium text-slate-500{% endif %}">
                    Catalogue
                </span>
            </a>

            <!-- 4. Stocks & Alertes -->
            <a href="{% url 'backoffice:stocks' %}" 
               class="flex flex-col items-center justify-center flex-1 py-1 transition-transform duration-100 active:scale-88 relative {% if current_page == 'stocks' %}text-amber-600{% else %}text-slate-400 hover:text-slate-700{% endif %}">
                <div class="relative flex items-center justify-center">
                    <svg class="w-5 h-5 {% if current_page == 'stocks' %}stroke-[2.2] text-amber-500{% else %}stroke-[1.8]{% endif %}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 12h16.5m-16.5 3.75h16.5M3.75 19.5h16.5M5.625 4.5h12.75a1.875 1.875 0 010 3.75H5.625a1.875 1.875 0 010-3.75z" />
                    </svg>
                    {% if low_stock_count and low_stock_count > 0 %}
                    <span class="absolute -top-1.5 -right-2 min-w-[17px] h-[17px] px-1 bg-rose-500 text-white font-black text-[9px] flex items-center justify-center rounded-full shadow-xs">
                        {{ low_stock_count }}
                    </span>
                    {% endif %}
                    {% if current_page == 'stocks' %}
                    <span class="w-1.5 h-1.5 rounded-full bg-amber-500 absolute -bottom-1"></span>
                    {% endif %}
                </div>
                <span class="text-[10px] tracking-tight leading-none mt-1 {% if current_page == 'stocks' %}font-black text-amber-600{% else %}font-medium text-slate-500{% endif %}">
                    Stocks
                </span>
            </a>

            <!-- 5. Menu Plus (Ouvre le Drawer complet) -->
            <button type="button" 
                    @click="mobileMenuOpen = !mobileMenuOpen" 
                    class="flex flex-col items-center justify-center flex-1 py-1 transition-transform duration-100 active:scale-88 relative cursor-pointer"
                    :class="mobileMenuOpen ? 'text-amber-600' : 'text-slate-400 hover:text-slate-700'">
                <div class="relative flex items-center justify-center">
                    <svg class="w-5 h-5 stroke-[1.8]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                    </svg>
                    <span x-show="mobileMenuOpen" class="w-1.5 h-1.5 rounded-full bg-amber-500 absolute -bottom-1"></span>
                </div>
                <span class="text-[10px] tracking-tight leading-none mt-1 font-medium" :class="mobileMenuOpen ? 'font-black text-amber-600' : 'text-slate-500'">
                    Menu
                </span>
            </button>

        </div>
    </nav>"""

content_lf = content_lf[:dock_start_pos] + new_light_dock + content_lf[dock_end_pos:]

final_base = content_lf.replace('\n', '\r\n') if is_crlf else content_lf
with open(base_path, 'w', encoding='utf-8') as f:
    f.write(final_base)

print("1. base.html updated with Light Frosted Glass Header and Bottom Dock!")

# -------------------------------------------------------------
# 2. Update templates/backoffice/stocks.html for Ultra Mobile Responsiveness
# -------------------------------------------------------------
stocks_path = os.path.join('templates', 'backoffice', 'stocks.html')
with open(stocks_path, 'r', encoding='utf-8') as f:
    stocks_content = f.read()

is_crlf_stocks = '\r\n' in stocks_content
stocks_lf = stocks_content.replace('\r\n', '\n')

# 2a. Make the 3 KPI cards responsive side-by-side (grid-cols-3) on mobile
old_kpi = """    <!-- 3 KPI STOCKS COMPACTS -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div class="bg-white p-3 rounded-lg border border-slate-200">
            <div class="text-[11px] font-semibold uppercase tracking-wider text-slate-500">Références Suivies</div>
            <div class="text-lg font-bold text-slate-900 mt-0.5 tabular-nums">
                {{ total_tracked_products }} <span class="text-[11px] font-normal text-slate-400">produits actifs</span>
            </div>
        </div>

        <div class="bg-white p-3 rounded-lg border border-slate-200">
            <div class="text-[11px] font-semibold uppercase tracking-wider text-slate-500">Ruptures Immédiates</div>
            <div class="text-lg font-bold {% if out_of_stock_count > 0 %}text-rose-600{% else %}text-slate-900{% endif %} mt-0.5 tabular-nums">
                {{ out_of_stock_count }} <span class="text-[11px] font-normal text-slate-400">articles à zéro</span>
            </div>
        </div>

        <div class="bg-white p-3 rounded-lg border border-slate-200">
            <div class="text-[11px] font-semibold uppercase tracking-wider text-slate-500">Stock Inférieur au Seuil</div>
            <div class="text-lg font-bold {% if low_stock_count > 0 %}text-amber-600{% else %}text-slate-900{% endif %} mt-0.5 tabular-nums">
                {{ low_stock_count }} <span class="text-[11px] font-normal text-slate-400">réassorts urgents</span>
            </div>
        </div>
    </div>"""

new_kpi = """    <!-- 3 KPI STOCKS RESPONSIVE EN GRILLE COMPACTE (STYLE APPLE WIDGETS) -->
    <div class="grid grid-cols-3 gap-2 sm:gap-3">
        <div class="bg-white p-2.5 sm:p-3.5 rounded-xl border border-slate-200/90 shadow-2xs">
            <div class="text-[9px] sm:text-[11px] font-bold uppercase tracking-wider text-slate-500 truncate">Références</div>
            <div class="text-base sm:text-2xl font-black text-slate-900 mt-0.5 tabular-nums font-heading">
                {{ total_tracked_products }}
            </div>
            <div class="text-[10px] text-slate-400 truncate hidden sm:block">produits actifs</div>
        </div>

        <div class="bg-white p-2.5 sm:p-3.5 rounded-xl border border-slate-200/90 shadow-2xs">
            <div class="text-[9px] sm:text-[11px] font-bold uppercase tracking-wider text-slate-500 truncate">Ruptures</div>
            <div class="text-base sm:text-2xl font-black {% if out_of_stock_count > 0 %}text-rose-600{% else %}text-slate-900{% endif %} mt-0.5 tabular-nums font-heading">
                {{ out_of_stock_count }}
            </div>
            <div class="text-[10px] text-slate-400 truncate hidden sm:block">articles à zéro</div>
        </div>

        <div class="bg-white p-2.5 sm:p-3.5 rounded-xl border border-slate-200/90 shadow-2xs">
            <div class="text-[9px] sm:text-[11px] font-bold uppercase tracking-wider text-slate-500 truncate">Stock Faible</div>
            <div class="text-base sm:text-2xl font-black {% if low_stock_count > 0 %}text-amber-600{% else %}text-slate-900{% endif %} mt-0.5 tabular-nums font-heading">
                {{ low_stock_count }}
            </div>
            <div class="text-[10px] text-slate-400 truncate hidden sm:block">réassorts urgents</div>
        </div>
    </div>"""

if old_kpi in stocks_lf:
    stocks_lf = stocks_lf.replace(old_kpi, new_kpi, 1)
    print("2a. KPI cards updated to responsive 3-column layout.")

# 2b. Smooth scroll filters
old_filters = """    <!-- FILTRES D'URGENCE COMPACTS -->
    <div class="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none text-xs">"""

new_filters = """    <!-- FILTRES D'URGENCE CAROUSEL SANS SCROLLBAR -->
    <div class="flex items-center gap-1.5 overflow-x-auto pb-1 no-scrollbar text-xs">"""

if old_filters in stocks_lf:
    stocks_lf = stocks_lf.replace(old_filters, new_filters, 1)
    print("2b. Filter bar scrollbar removed.")

# 2c. Table search header: stack vertically on mobile
old_table_header = """        <div class="p-2.5 border-b border-slate-200 flex items-center justify-between gap-3 bg-slate-50/50">
            <span class="text-xs font-bold text-slate-900 uppercase tracking-wider">État des Réserves en Entrepôt</span>
            <form method="GET" class="relative max-w-xs w-full">"""

new_table_header = """        <div class="p-2.5 sm:p-3 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 bg-slate-50/50">
            <span class="text-xs font-bold text-slate-900 uppercase tracking-wider">État des Réserves en Entrepôt</span>
            <form method="GET" class="relative w-full sm:max-w-xs">"""

if old_table_header in stocks_lf:
    stocks_lf = stocks_lf.replace(old_table_header, new_table_header, 1)
    print("2c. Table header search made 100% full width on mobile.")

# 2d. Table min-w-[580px] to preserve column structure on swipe
old_table = """            <table class="w-full text-left text-xs border-collapse">"""
new_table = """            <table class="w-full text-left text-xs border-collapse min-w-[560px]">"""

if old_table in stocks_lf:
    stocks_lf = stocks_lf.replace(old_table, new_table, 1)
    print("2d. Table set to min-w-[560px] with smooth horizontal swipe.")

final_stocks = stocks_lf.replace('\n', '\r\n') if is_crlf_stocks else stocks_lf
with open(stocks_path, 'w', encoding='utf-8') as f:
    f.write(final_stocks)

print("2. stocks.html successfully updated with ultra-responsive mobile layout!")
