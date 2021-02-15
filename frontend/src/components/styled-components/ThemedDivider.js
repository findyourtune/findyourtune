import styled from 'vue-styled-components';

const themeProps = { color: String };

const ThemedDivider = styled('hr', themeProps)`
  background-color: ${props => props.color};
`;

export default ThemedDivider;