(function() {

    // Components

    // Pages
    var Index = Vue.extend({
        template: '#index',
        props: ['storage']
    });

    var Articles = Vue.extend({
        template: '#articles',
        props: ['storage'],
        data: function () {
            return {
                articles: this.storage.user.data.articles
            };
        }
    });

    var Article = Vue.extend({
        template: '#article',
        props: ['storage'],
        route: {
            data: function (transition) {
                var articles = this.storage.user.data.articles;
                var index = null;
                for(var i in articles) {
                    if(articles[i].id == transition.to.params.id) {
                        index = i;
                        break;
                    }
                }
                this.article = this.storage.user.data.articles[i];
                transition.next();
            }
        },
        data: function () {
            return {
                article: {}
            };
        }
    });

    var About = Vue.extend({
        template: '#about'
    });

    var Login = Vue.extend({
        template: '#login',
        data: function () {
            return {
                email: '',
                password: ''
            };
        },
        methods: {
            login: function () {}
        }
    });

    var Register = Vue.extend({
        template: '#register',
        data: function () {
            return {
                email: '',
                password: '',
                passwordVerify: ''
            };
        },
        methods: {
            register: function () {}
        }
    });

    var NotFound = Vue.extend({
        template: '#not-found'
    });

    // Router
    var Root = Vue.extend({
        compiled: function () {
            Vue.http.get('/api/read/user', {
                token: 'temp'
            })
            .then(function (response) {
                console.log(response);
            },
            function (error) {
                console.log(error);
            });
        },
        data: function () {
            return {
                storage: {
                    user: {
                        info: {
                            name: 'test testerson'
                        },
                        data: {
                            articles: [
                                {
                                    id: 1,
                                    title: 'article 1',
                                    body: 'Lorem ipsum dolor sit amet, deleniti consulatu ius no. Ei noster voluptatum quo. Et propriae voluptatum sed. Has tale eloquentiam definitionem an, sit prompta consulatu interesset eu. At sale nonumy officiis eam.'
                                },
                                {
                                    id: 2,
                                    title: 'article 2',
                                    body: 'Te sea wisi posse veniam, ius cu dico affert omnesque. Mel latine alterum repudiare ad, at sea nulla aliquid. In nam persius commune, at soleat cotidieque eos. Sale everti cu sit, ea per indoctum mediocrem interpretaris.'
                                },
                                {
                                    id: 3,
                                    title: 'article 3',
                                    body: 'Ea vim aperiam saperet. Vim liber omnesque luptatum ex, ne dicam graeco adversarium mel, decore detracto ea qui. Mei ad vide aliquam lucilius, est eu quas iuvaret. Ex viris incorrupte nec, eu aeque dolor per. Ne error elitr tollit has, iusto omittam aliquando id duo.'
                                }
                            ]
                        }
                    },
                    userLoggedIn: true
                }
            };
        }
    });

    var router = new VueRouter({
        hashbang: false,
        history: true
    });

    router.map({
        '/': {
            name: 'index',
            component: Index
        },
        '/about': {
            name: 'about',
            component: About
        },
        '/articles': {
            name: 'articles',
            component: Articles
        },
        '/article/:id': {
            name: 'article',
            component: Article
        },
        '/login': {
                name: 'login',
                component: Login
        },
        '/register': {
            name: 'register',
            component: Register
        },
        '/404': {
            name: '404',
            component: NotFound
        }
    });

    router.start(Root, '#app');
})();