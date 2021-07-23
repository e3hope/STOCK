// action types
const LOGIN = "LOGIN";
const LOGOUT = "LOGOUT";
const EDIT_USER = "EDIT_USER";

// action creators
export const login = (params) => ({ type: LOGIN, payload: params });
export const logout = () => ({ type: LOGOUT, payload: {} });
export const editUser = (params) => ({ type: EDIT_USER, payload: params });

// reducers
export const reducer = (state, action) => {
  const { type, payload } = action;
  switch (type) {
    /* user */
    // 로그인
    case LOGIN:
      state = { ...state, user: payload };
      return state;
    // 로그아웃
    case LOGOUT:
      state = { ...state, user: null };
      return state;
    // 내 정보 수정
    case EDIT_USER:
      if (action.payload) {
        state = { ...state, user: { ...state.user, ...action.payload } };
      }
      return state;
    default:
      return state;
  }
};
