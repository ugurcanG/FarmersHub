export const formatDateTime = (isoString: string): string => {
  if (!isoString) return ''

  return new Date(isoString).toLocaleString('de-DE', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export const formatDate = (isoString: string): string => {
  if (!isoString) return ''

  return new Date(isoString).toLocaleDateString('de-DE', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
}
