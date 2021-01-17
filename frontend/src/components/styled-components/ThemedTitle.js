import styled from 'vue-styled-components';

const themeProps = { color: String };

const ThemedTitle = styled('h1', themeProps)`
  color: ${props => props.color};
  border-bottom: 1px solid ${props => props.color};
  margin-bottom: 2em;
  padding-bottom: 10px;
`;

export default ThemedTitle;