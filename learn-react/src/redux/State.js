
let state = {
    profilePage: {
        posts: [
            {id: 1, message: 'Hello', likesCount: 5},
            {id: 2, message: 'How are you', likesCount: 25},
        ],
    },
    messagesPage: {
        dialogs: [
            {id: 1, name: 'Sasha', url: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSUWRy6ZeIRHk3Xl-8bRvKaUtJCuee08y8Asg&usqp=CAU'},
            {id: 2, name: 'Vlad', url: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSlrZqTCInyg6RfYC7Ape20o-EWP1EN_A8fOA&usqp=CAU'},
            {id: 3, name: 'Sveta', url: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNU22TXbkcX-uklS2Ebx_xS-lBNJCKHNFiIQ&usqp=CAU'},
            {id: 4, name: 'Vika', url: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ3Qe0kqKqUiuTBcNLMnIEuigg6DhN3uqRseg&usqp=CAU'},
        ],


        messages: [
            {id: 1, message: 'Hi'},
            {id: 2, message: 'How are you?'},
            {id: 3, message: 'Hi'},
            {id: 4, message: 'How are you?'},
        ],
    },
}

export default state;
